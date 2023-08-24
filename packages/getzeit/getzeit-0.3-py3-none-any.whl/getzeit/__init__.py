#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
#
# getzeit: Download DIE ZEIT newspaper in various formats
# Copyright 2021, 2023 mahlzahn <mahlzahn@posteo.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

PROG_NAME = 'getzeit'

import argparse
argcomplete_available = True
try:
    import argcomplete
except ImportError:
    argcomplete_available = False

import browser_cookie3
import datetime
import http
import importlib.metadata
import os
import pathlib
import pickle
import requests
import shutil
import subprocess
import time

PAGES = {
        'zeit+magazin': 'DIE ZEIT gesamt',
        'zeit': 'DIE ZEIT',
        'magazin': 'ZEITmagazin',
        'cuw': 'Christ & Welt',
        'hamburg': 'ZEIT Hamburg',
        'osten': 'ZEIT Osten',
        'oesterreich': 'ZEIT Österreich',
        'schweiz': 'ZEIT Schweiz',
        'campus': 'ZEIT Campus',
        }

def _get_what(pages=None):
    """Get the type of journal for given pages"""
    try:
        pages = int(pages)
    except ValueError:
        pass
    if type(pages) == int:
        try:
            return _get_what(list(PAGES)[pages])
        except IndexError:
            raise ValueError(f'Given pages must be >= 0 and < {len(PAGES)}')
    if pages == 'campus':
        return 'zeitcampus'
    if pages in list(PAGES) or pages is None:
        return 'diezeit'
    return pages

def _get_size(file_path):
    size = os.path.getsize(file_path)
    for unit in ['B', 'KiB', 'MiB', 'GiB', 'TiB']:
        if size < 1024 or unit == 'TiB':
            break
        size /= 1024
    return f'{size:.1f} {unit}'

def parse_args(args=None):
    metadata = importlib.metadata.distribution(PROG_NAME).metadata
    parser = argparse.ArgumentParser(
            prog=PROG_NAME,
            description=metadata['Summary'],
            epilog="""
Depending on the given parameters --issue, --year, --month and --day, one or multiple issues will be downloaded:

| issue | year | month | day  | which issue(s) will be downloaded?
| ----- | ---- | ----- | ---- | ---------------------------------------------------
| ISSUE | YEAR | ...   | ...  | only issue ISSUE of year YEAR
| ISSUE | None | ...   | ...  | only issue ISSUE of current year
| None  | YEAR | MONTH | DAY  | only one of day DAY in month MONTH and year YEAR
| None  | None | MONTH | DAY  | only one of day DAY in month MONTH and current year
| None  | None | None  | DAY  | only one of day DAY in current month and year
| None  | None | None  | None | only current issue
| None  | YEAR | None  | None | all issues of year YEAR (issue 01 to last issue)
| None  | YEAR | MONTH | None | all issues of month MONTH in year YEAR
| None  | None | MONTH | None | all issues of month MONTH in current year
| None  | YEAR | None  | DAY  | none""",
            formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-i', '--issue', type=int,
            help='The number of the issue, if given then --month and --day are ignored')
    parser.add_argument('-y', '--year', type=int, help='The year of the issue(s)')
    parser.add_argument('-m', '--month', type=int, help='The month of the issue(s)')
    parser.add_argument('-d', '--day', type=int, help='The day of the issue')
    parser.add_argument('-f', '--format', choices=['pdf', 'epub', 'jpg'],
            default='pdf',
            help="The file format, if 'jpg' the title page is downloaded")
    parser.add_argument('-p', '--pages', default='0',
            help="The type of pages to be downloaded for 'pdf' or 'jpg' download: "
                    + ', '.join(f'{i}: {PAGES[p]}' for i, p in enumerate(PAGES))
                    + '. This is ignored for the epub download')
    parser.add_argument('-o', '--output', type=pathlib.Path,
            help="The output file path for a single issue or output directory for multiple issues. In case of a single issue, the ending should match the given '--format'")
    parser.add_argument('-r', '--recreate-cookie-jar', action='store_true',
            help="Recreate the session with cookies in the pickled cookie jar file definded by the option '--cookie_jar_file'")
    parser.add_argument('-c', '--cookie-jar-file', type=pathlib.Path,
            default=f'~/.cache/{PROG_NAME}/cookie_jar.pkl',
            help='The path of the pickled cookie jar file to be used to store or read the session cookies with login information')
    parser.add_argument('-b', '--browser', type=str, default='firefox',
            help='The browser to be used for the login process to get session cookies')
    parser.add_argument('-n', '--dry-run', action='store_true',
            help='Perform a trial run without download')
    parser.add_argument('-v', '--version', action='version',
            version=f"{PROG_NAME} {metadata['Version']}")
    if argcomplete_available:
        argcomplete.autocomplete(parser)
    args = parser.parse_args(args)
    try:
        if int(args.pages) not in range(len(PAGES)):
            parser.error(f"argument -p/--pages: invalid value: '{args.pages}'")
    except ValueError:
        pass
    return args

def create_cookie_jar(browser='firefox',
        cookie_jar_file=f'~/.cache/{PROG_NAME}/cookie_jar.pkl',
        login_url='https://meine.zeit.de', domain_name='zeit.de'):
    browser_tmp_dir = f'/tmp/{PROG_NAME}_browser_cookie3'
    os.makedirs(browser_tmp_dir, exist_ok=True)
    browser_x = browser.lower()
    if browser_x.endswith('.exe'):
        browser_x = browser_x[:-4]
    if browser_x.endswith('chrome'):
        subprocess.run([browser, f"--user-data-dir={browser_tmp_dir}",
                '-kiosk', login_url])
        cookie_jar = browser_cookie3.chrome(
                cookie_file=f"{browser_tmp_dir}/Default/Cookies",
                domain_name=domain_name)
    elif any([browser_x.endswith(b) for b in ['chromium', 'chromium-browser']]):
        subprocess.run([browser, f"--user-data-dir={browser_tmp_dir}",
                '-kiosk', login_url])
        cookie_jar = browser_cookie3.chromium(
                cookie_file=f"{browser_tmp_dir}/Default/Cookies",
                domain_name=domain_name)
    elif any([browser_x.endswith(b) for b in ['firefox', 'librewolf']]):
        subprocess.run([browser, '--profile', browser_tmp_dir, '--kiosk',
                login_url])
        cookie_jar = browser_cookie3.FirefoxBased(browser,
                cookie_file=f"{browser_tmp_dir}/cookies.sqlite",
                domain_name=domain_name).load()
    elif browser_x.endswith('w3m'):
        env = os.environ.copy()
        env['W3M_DIR'] = browser_tmp_dir
        subprocess.run([browser, '-cookie', login_url], env=env)
        cookie_jar = browser_cookie3.W3m(
                cookie_file=f"{browser_tmp_dir}/cookie",
                domain_name=domain_name).load()
    elif browser_x.endswith('lynx'):
        cfg_file = f"{browser_tmp_dir}/lynx.cfg"
        cookie_file = f"{browser_tmp_dir}/cookies"
        with open(cfg_file, 'w') as f:
            subprocess.run([browser, '-show_cfg'], stdout=f)
            f.write("ACCEPT_ALL_COOKIES:TRUE\nPERSISTENT_COOKIES:TRUE\n"
                    f"COOKIE_FILE:{cookie_file}")
            # TODO: check what happens if these options were specified in default
            # lynx cfg
        subprocess.run([browser, '-cfg', cfg_file, login_url])
        cookie_jar = browser_cookie3.Lynx(
                cookie_file=f"{browser_tmp_dir}/cookies",
                domain_name=domain_name).load()
    else:
        raise RuntimeError(
                f'Given browser {browser} is not supported')
    # Convert cookie jar to RequestsCookieJar which can be pickled and save it
    cookie_jar = requests.cookies.merge_cookies(
            requests.cookies.RequestsCookieJar(), cookie_jar)
    os.makedirs(os.path.dirname(cookie_jar_file), exist_ok=True)
    if cookie_jar_file is not None:
        cookie_jar_file = os.path.expanduser(cookie_jar_file)
        pickle.dump(cookie_jar, open(cookie_jar_file, 'wb'))
    shutil.rmtree(browser_tmp_dir)
    return cookie_jar

def retrieve_cookie_jar(cookie_jar_file=f'~/.cache/{PROG_NAME}/cookie_jar.pkl'):
    cookie_jar_file = os.path.expanduser(cookie_jar_file)
    return pickle.load(open(cookie_jar_file, 'rb'))

def _get_date(year, month=1, day=1):
    if int(year) < 100:
        year = f'20{int(year):02d}'
    return f'{int(day):02d}.{int(month):02d}.{year}'

def _get_url(url, base_url=None):
    if url.startswith('/'):
        return f'{base_url}{url}'
    return url

class ZeitDownload:
    def __init__(self, url, file_format=None, title=None, pages_type=None,
            size=None):
        self.url = url
        self.file_format = file_format
        self.title = title
        self.pages_type = pages_type
        self.size = size

    def __str__(self):
        string = self.url
        if self.title:
            string = f'{self.title} at {string}'
        elif self.pages_type:
            string = f'{self.pages_type} at {string}'
        if self.file_format and self.size:
            string += f' ({self.file_format}, {self.size})'
        elif self.file_format:
            string += f' ({self.file_format})'
        elif self.size:
            string += f' ({self.size})'
        return string

class ZeitIssue:
    def __init__(self, url, title, image_url=None):
        self.url = url
        self.title = title
        self.image_url = image_url
        self.date = url.split('/')[-1]
        self.day, self.month, self.year = [int(x) for x in self.date.split('.')]
        journal_title_issue, issue_year = title.split('/')
        self.issue_year = int(issue_year)
        *journal_title, issue = journal_title_issue.split(' ')
        self.issue = int(issue)
        self.journal_title = ' '.join(journal_title)

    def __str__(self):
        return f'{self.title} from {self.date}'

    def parse_downloads_overview(self, overview_request):
        base_url = '/'.join(overview_request.url.split('/')[:3])
        _, issue_title_full = overview_request.text.split(
                '<span class="article-teaser-issue">', 1)
        issue_title_full, _ = issue_title_full.split('</span>', 1)
        issue_title_full = issue_title_full.strip()
        issue_title, issue_date = issue_title_full.split(' vom ')
        issue_issue_title = issue_title[:issue_title.rfind(' ')]
        issue_issue_year = issue_title[issue_title.rfind(' ') + 1:]
        pdf = {}
        jpg = {}
        epub = {}
        for line in overview_request.text.split('<div class="epaper "')[1:]:
            image_url, line = line.split(' src="', 1)[1].split('"', 1)
            title, line = line.split('<p class="epaper-info-title pull-left">',
                    1)[1].split('<', 1)
            title = title.replace('&amp;', '&').strip()
            url, line = line.split('href="', 1)[1].split('"', 1)
            pages_type, line = line.split('#download_', 1)[1].split("'", 1)
            size, line = line.split('</i> ', 1)[1].split('<', 1)
            if not pages_type:
                pages_type = title.lower()
            if not title.endswith(issue_issue_year):
                title = f'{title} {issue_issue_year}'
            pdf[pages_type] = ZeitDownload(_get_url(url, base_url), 'pdf',
                    title, pages_type, size)
            jpg[pages_type] = ZeitDownload(_get_url(image_url, base_url), 'jpg',
                    title, pages_type)
            if pages_type == 'zeit':
                pdf['diezeit'] = pdf[pages_type]
                jpg['diezeit'] = jpg[pages_type]
                jpg['zeit+magazin'] = jpg[pages_type]
            if not pages_type.startswith('zeit'):
                pdf[f'zeit{pages_type}'] = pdf[pages_type]
                jpg[f'zeit{pages_type}'] = jpg[pages_type]
        line_x = overview_request.text.split('<div class="download-buttons">')
        if len(line_x) > 1:
            for line in line_x[1].split('href="')[1:]:
                url, line = line.split('"', 1)
                pages_type, line = line.split('#download_', 1)[1].split("'", 1)
                file_format, line = line.split("9: '", 1)[1].split("'", 1)
                line_x = line.split('<span class="text-normal">(', 1)
                size = line_x[1].split(')', 1)[0] if len(line_x) == 2 else None
                if file_format == 'pdf':
                    title = f'{issue_issue_title} gesamt {issue_issue_year}'
                    pdf[pages_type] = ZeitDownload(_get_url(url, base_url), 'pdf',
                            title, pages_type, size)
                    if not pages_type.startswith('zeit'):
                        pdf[f'zeit{pages_type}'] = pdf[pages_type]
                elif file_format == 'epub':
                    title = f'{issue_issue_title} {issue_issue_year}'
                    epub[pages_type] = ZeitDownload(_get_url(url, base_url), 'epub',
                            title, pages_type, size)
                    epub['zeit'] = epub[pages_type]
                    epub['diezeit'] = epub[pages_type]
                    if not pages_type.startswith('zeit'):
                        epub[f'zeit{pages_type}'] = epub[pages_type]
        self.downloads = dict(pdf=pdf, jpg=jpg, epub=epub)

def get_zeit_issues_archive_html(archive_html):
    issues = []
    for line in archive_html.split('<div class="epaper "')[1:]:
        url, line = line.split('href="')[1].split('"', 1)
        image_url, line = line.split('<img src="')[1].split('"', 1)
        title, line = line.split('<p class="epaper-info-title">')[1].split(
                '</p>', 1)
        date = line.split('<p class="epaper-info-release-date">')[1].split(
                '</p>')[0]
        assert(date == url.split('/')[-1])
        issues.append(ZeitIssue(url=url, title=title, image_url=image_url))
    return issues

class ZeitSession(requests.Session):
    """Session class for retrieval of issues of ZEIT journals"""
    base_url = 'https://epaper.zeit.de'
    login_url = 'https://meine.zeit.de'
    archive_url = f'{base_url}/api/archives'
    abo_url = f'{base_url}/abo'

    def __init__(self, cookie_jar_file=f'~/.cache/{PROG_NAME}/cookie_jar.pkl',
            recreate_cookie_jar=False, browser='firefox', **kwargs):
        super().__init__(**kwargs)
        if recreate_cookie_jar:
            cookies = create_cookie_jar(browser, cookie_jar_file)
        else:
            try:
                cookies = retrieve_cookie_jar(cookie_jar_file)
            except FileNotFoundError:
                cookies = create_cookie_jar(browser, cookie_jar_file)
        if not any([c.name.startswith('zeit_sso') for c in cookies]):
            raise RuntimeError(
                    f'The authentification failed. You may try again with -r')
        self.cookies = requests.cookies.merge_cookies(self.cookies, cookies)
        # Cookie 'dzcookie' needed for use of archive
        if not any([c.name == 'dzcookie' and c.domain.find(domain) >= 0
                for c in self.cookies]):
            self.get(self.base_url)

    def get_issues_for_issue(self, issue=None, year=None, what='diezeit',
            raise_missing_issue_error=True):
        """Get issues for given issue number and year

        Returned issues depend on the given arguments (issue, year):
        * (i,    y   ) -> return [issue i of year y]
        * (i,    None) -> return [issue i of current year]
        * (None, y   ) -> return issues of year y
        * (None, None) -> return [current issue]

        Parameters
        ----------
        issue: int or str
            The issue number
        year: int or str
            The year, must be at least 2012
        what: str
            The type of journal e.g. 'diezeit', 'zeitcampus', etc.
        raise_missing_issue_error: bool
            Whether to raise RuntimeError when issue is not found in archive
        """
        # year may be in future, e.g., in the end of the year when issues are
        # already counted for the next year
        if year is not None:
            if int(year) < 1946:
                raise ValueError(f'In year {year} DIE ZEIT was not published, yet')
        # (None, None) -> return current issue
        elif issue is None:
            return self.get_issues_for_date(what=what,
                    raise_missing_issue_error=raise_missing_issue_error)
        year = year or time.gmtime().tm_year
        if issue is not None:
            issue = f'{int(issue):02d}'
        params = {'title': what, 'year': year, 'issue': issue}
        request = self.get(f'{self.abo_url}/{what}', params=params)
        request.raise_for_status()
        issues = get_zeit_issues_archive_html(
                request.text[request.text.find('Archiv'):])
        # (i,    y   ) -> return issue i of year y
        # (i,    None) -> return issue i of current year
        if issue is not None:
            if issues and issues[0].issue == int(issue):
                return issues[:1]
            if raise_missing_issue_error:
                raise RuntimeError(f'Issue {issue}/{year} not found in archive')
            return []
        # (None, y   ) -> return issues of year y
        if not issues:
            if raise_missing_issue_error:
                raise RuntimeError(
                        f'No issues for given year {year} found in archive')
            return []
        date_get_more_issues = issues[-1].date
        while date_get_more_issues:
            issues_more, no_more_issues = self._get_more_issues_before(
                    date_get_more_issues, what)
            issues.extend([i for i in issues_more if i.issue_year == int(year)])
            if not no_more_issues and issues_more \
                    and issues_more[-1].issue_year == int(year):
                date_get_more_issues = issues_more[-1].date
            else:
                date_get_more_issues = False
        return issues

    def get_issues_for_date(self, year=None, month=None, day=None, what='diezeit',
            raise_missing_issue_error=True):
        """Get issues for given year, month and day

        Returned issues depend on the given arguments (issue, year, month, day):
        * (y,    m,    d)    -> return [issue of day d in month m and year y]
        * (None, m,    d)    -> return [issue of day d in month m and current year]
        * (None, None, d)    -> return [issue of day d in current month and year]
        * (None, None, None) -> return [current issue]
        * (y,    None, d)    -> raise ValueError
        * (y,    m,    None) -> return issues of month m in year y
        * (None, m,    None) -> return issues of month m in current year
        * (y,    None, None) -> return issues of year y

        Parameters
        ----------
        issue: int or str
            The issue number
        year: int or str
            The year, must be at least 2012
        month: int
            The month, ignored if issue is given
        day: int
            The day, ignored if issue is given
        what: str
            The type of journal e.g. 'diezeit', 'zeitcampus', etc.
        raise_missing_issue_error: bool
            Whether to raise RuntimeError when issue is not found in archive
        """
        # ZEIT API allows non-existant dates such as 32.12.2000 as well as future
        # dates (e.g., issues can be downloaded already on the evening before)
        if year is not None:
            if int(year) < 1946:
                raise ValueError(f'In year {year} DIE ZEIT was not published, yet')
        # (None, None, None) -> return [current issue]
        elif month is None and day is None:
            issues, _ = self._get_more_issues_before(
                    _get_date(time.gmtime().tm_year + 1), what)
            if not issues and raise_missing_issue_error:
                raise RuntimeError(f'Current issue not found')
            return issues[:1]
        # (y,    None, d)    -> raise ValueError
        if year is not None and month is None and day is not None:
            raise ValueError('Day and year are given but month is not')
        year = int(year or time.gmtime().tm_year)
        if day is not None or month is not None:
            month = int(month or time.gmtime().tm_mon)
        # (y,    m,    d)    -> return [issue of day d in month m and year y]
        # (None, m,    d)    -> return [issue of day d in month m and current year]
        # (None, None, d)    -> return [issue of day d in current month and year]
        if day is not None:
            date = _get_date(year, month, day)
            issues, _ = self._get_more_issues_before(
                    _get_date(year, month, int(day) + 1), what)
            if not (issues and issues[0].date == date) \
                    and raise_missing_issue_error:
                raise RuntimeError(
                        f'No issue for given date {date} found in archive')
            return issues[:1]
        issues = []
        # (y,    m,    None) -> return issues of month m in year y
        # (None, m,    None) -> return issues of month m in current year
        if month is not None:
            date_get_more_issues = _get_date(year, int(month) + 1)
            while date_get_more_issues:
                issues_more, no_more_issues = self._get_more_issues_before(
                        date_get_more_issues, what)
                issues.extend([i for i in issues_more if i.year == int(year)
                        and i.month == int(month)])
                if not no_more_issues and issues_more \
                        and issues_more[-1].month == int(month):
                    date_get_more_issues = issues_more[-1].date
                else:
                    date_get_more_issues = False
            if not issues and raise_missing_issue_error:
                raise RuntimeError(
                        f'No issues for given month {month} in year {year} found'
                        ' in archive')
        # (y,    None, None) -> return issues of year y
        else:
            date_get_more_issues = _get_date(year + 1)
            while date_get_more_issues:
                issues_more, no_more_issues = self._get_more_issues_before(
                        date_get_more_issues, what)
                issues.extend([i for i in issues_more if i.year == int(year)])
                if not no_more_issues and issues_more \
                        and issues_more[-1].year == int(year):
                    date_get_more_issues = issues_more[-1].date
                else:
                    date_get_more_issues = False
            if not issues and raise_missing_issue_error:
                raise RuntimeError(
                        f'No issues for given year {year} found in archive')
        return issues

    def get_issues(self, issue=None, year=None, month=None, day=None,
            what='diezeit', raise_missing_issue_error=True):
        """Get issues for given issue, year, month and day

        Returned issues depend on the given arguments. If issue is given, then month
        and day are ignored the returned issues depend only on (issue, year):
        * (i,    y   ) -> return [issue i of year y]
        * (i,    None) -> return [issue i of current year]
        If issue is not given then the returned issues depend on (year, month, day):
        * (y,    None, None) -> return issues of year y (issue 01 to last issue)
        * (y,    m,    d)    -> return [issue of day d in month m and year y]
        * (None, m,    d)    -> return [issue of day d in month m and current year]
        * (None, None, d)    -> return [issue of day d in current month and year]
        * (None, None, None) -> return [current issue]
        * (y,    None, d)    -> raise ValueError
        * (y,    m,    None) -> return issues of month m in year y
        * (None, m,    None) -> return issues of month m in current year

        Parameters
        ----------
        year: int or str
            The year, must be at least 2012
        month: int
            The month, ignored if issue is given
        day: int
            The day, ignored if issue is given
        what: str
            The type of journal e.g. 'diezeit', 'zeitcampus', etc.
        raise_missing_issue_error: bool
            Whether to raise RuntimeError when issue is not found in archive
        """
        if issue is not None or day is None and month is None:
            return self.get_issues_for_issue(issue=issue, year=year, what=what,
                    raise_missing_issue_error=raise_missing_issue_error)
        return self.get_issues_for_date(year=year, month=month, day=day, what=what,
                raise_missing_issue_error=raise_missing_issue_error)

    def _get_more_issues_before(self, date, what='diezeit'):
        """Get more issues before given date

        Parameters
        ----------
        date: str
            Date in format '%d.%m.%Y'
        what: str
            The type of journal e.g. 'diezeit', 'zeitcampus', etc.

        Returns
        -------
        issues: list(getzeit.ZeitIssue)
            A bunch of up to 5 issues found before the given date
        no_more_issues: bool
            Whether no more issues than the returned are found before the given date
        """
        request = self.get(f'{self.archive_url}/{what}/{date}/load-more.json')
        request.raise_for_status()
        issues = get_zeit_issues_archive_html(request.json()['htmlContent'])
        return issues, request.json()['noMoreResults']

    def download_issue(self, issue, file_format='pdf', pages_type=0,
            output=None, dry_run=False, raise_missing_download_error=True):
        """Download given issue

        Parameters
        ----------
        issue: getzeit.ZeitIssue
            The issue
        file_format: {'epub', 'pdf', 'jpg'}
            The format of the electronic book, if jpg download the title page
        pages_type: int or str
            The type of pages to be downloaded for pdf or jpg download:
            0 for DIE ZEIT and ZEITmagazin, 1 for DIE ZEIT only,
            2 for ZEITmagazin only, 3 for Christ & Welt, 4 for ZEIT im Osten,
            5 for ZEIT Österreich, 6 for ZEIT Schweiz, 8 for ZEIT Hamburg
            This is ignored for the epub download, which includes all but
            Christ & Welt by default
        output: str
            The output file or directory path. In case of a file path, the ending
            should match the given 'file_format'
        dry_run: bool
            Whether to perform a trial run without download
        """
        try:
            pages_type = int(pages_type)
        except ValueError:
            pass
        if type(pages_type) == int:
            pages_type = list(PAGES)[pages_type]
            issue_title = PAGES[pages_type]
        else:
            issue_title = pages_type
        try:
            issue.downloads
        except AttributeError:
            issue_overview_request = self.get(_get_url(issue.url, self.base_url))
            issue_overview_request.raise_for_status()
            issue.parse_downloads_overview(issue_overview_request)
        try:
            download = issue.downloads[file_format][pages_type]
            if output and os.path.basename(output).lower().endswith(file_format):
                output_file = output
            else:
                date_formatted = f'{issue.year}_{issue.month:02d}_{issue.day:02d}'
                title_formatted = download.title.replace(' ', '_').replace('/', '_')
                output_file = f'{date_formatted}_{title_formatted}.{file_format}'
                if output:
                    output_file = os.path.join(output, output_file)
                    if not dry_run:
                        os.makedirs(output, exist_ok=True)
            if dry_run:
                print(f'INFO: Found {download} from {issue.date}')
                return
            with open(output_file, 'wb') as f:
                f.write(self.get(_get_url(download.url, self.base_url)).content)
                print(f'INFO: Saved {download.title} from {issue.date} to '
                        + f'{output_file} ({_get_size(output_file)})')
        except KeyError:
            message = f'No {file_format} download found for ' \
                    + f'{issue_title} {issue.issue}/{issue.issue_year}'
            if raise_missing_download_error:
                raise RuntimeError(message)
            print(f'INFO: {message}')

def main():
    args = parse_args()
    with ZeitSession(args.cookie_jar_file, args.recreate_cookie_jar, args.browser) \
            as session:
        issues = session.get_issues(issue=args.issue, year=args.year,
                month=args.month, day=args.day, what=_get_what(args.pages),
                raise_missing_issue_error=True)
        if len(issues) > 1 and args.output is not None:
            os.makedirs(args.output, exist_ok=True)
        for issue in issues:
            session.download_issue(issue=issue, file_format=args.format,
                    pages_type=args.pages, output=args.output, dry_run=args.dry_run,
                    raise_missing_download_error=False)

if __name__ == "__main__":
    main()

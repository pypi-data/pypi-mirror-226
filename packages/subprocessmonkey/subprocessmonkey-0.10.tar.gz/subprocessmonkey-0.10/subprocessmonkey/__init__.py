import _winapi
import itertools
import os
import pathlib
import platform
import re
import sys
import warnings
from ctypes import wintypes
import ctypes
from ctypes import WinDLL
from functools import cache
import subprocess
import pickle

subprocconfig = sys.modules[__name__]
subprocconfig.minlen = None
subprocconfig.convert_to_abs_path = True

try:
    windll = ctypes.LibraryLoader(WinDLL)
    user32 = windll.user32
    kernel32 = windll.kernel32

    GetWindowRect = user32.GetWindowRect
    GetClientRect = user32.GetClientRect
    _GetShortPathNameW = kernel32.GetShortPathNameW
    _GetShortPathNameW.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD]
    _GetShortPathNameW.restype = wintypes.DWORD
except ImportError:
    pass

forbiddennames = r"""(?:CON|PRN|AUX|NUL|COM0|COM1|COM2|COM3|COM4|COM5|COM6|COM7|COM8|COM9|LPT0|LPT1|LPT2|LPT3|LPT4|LPT5|LPT6|LPT7|LPT8|LPT9)"""
compregex = re.compile(rf"(^.*?\\?)?\b{forbiddennames}\b(\.?[^\\]*$)?", flags=re.I)
forbiddenchars = {"<", ">", ":", '"', "|", "?", "*"}
allcontrols_s = {
    "\x00",
    "\x01",
    "\x02",
    "\x03",
    "\x04",
    "\x05",
    "\x06",
    "\x07",
    "\x08",
    "\x09",
    "\x0a",
    "\x0b",
    "\x0c",
    "\x0d",
    "\x0e",
    "\x0f",
    "\x10",
    "\x11",
    "\x12",
    "\x13",
    "\x14",
    "\x15",
    "\x16",
    "\x17",
    "\x18",
    "\x19",
    "\x1a",
    "\x1b",
    "\x1c",
    "\x1d",
    "\x1e",
    "\x1f",
}


@cache
def inforbidden(x):
    return x in forbiddenchars or x in allcontrols_s


def check_if_space(text):
    def tw(x):
        return x == " "

    left = len(list(itertools.takewhile(tw, text)))
    right = len(list(itertools.takewhile(tw, list(reversed(text)))))
    return left, right


def get_path_from_string(t, minlen=None, convert_to_abs_path=True):
    wholestring = t
    if not minlen:
        minlen = (
            len(
                sorted(
                    [
                        x
                        for x in re.split(r"[\\/]+", t)
                        if not (g := set(x)).intersection(allcontrols_s)
                        and not g.intersection(forbiddenchars)
                        and not compregex.match(x)
                    ],
                    key=lambda q: len(q),
                )[0]
            )
            + 1
        )

    def _get_path_from_string(lis):
        allresults = []
        lastin = 0
        templist = lis.copy()
        abscounter = 0
        while True:
            somethinfound = False
            lastpath = ""
            for la in range(0, len(templist)):
                for q in range(1, len(templist) + 1):
                    if q - la < minlen:
                        continue
                    joix = templist[la:q]

                    if "\\" not in joix and "/" not in joix:
                        continue

                    joi = "".join(joix)
                    ##print(joi)
                    if os.path.exists(joi):
                        lastpath = joi
                        lastin = q
                        somethinfound = True
                    if lastpath:
                        if inforbidden(joi[-1]):
                            break

                if lastpath:
                    templist = templist[lastin:]
                    allresults.append(
                        (
                            lastin - len(lastpath) + abscounter,
                            lastin + abscounter,
                            lastpath,
                        )
                    )
                    # print(f'{lastpath=}')
                    abscounter = lastin + abscounter
                    lastin = 0
                    break
            if not somethinfound:
                break

        return allresults

    lis = list(t)
    laazx = _get_path_from_string(lis)
    allres = []
    wholestringnew = []
    ini = 0
    lastindi = 0
    for s, e, text in laazx:
        sta, end = check_if_space(text)
        # print(text)
        endx = end * " "
        s += sta
        e -= end

        longname = wholestring[s:e]
        # print(wholestring)
        if convert_to_abs_path:
            if not ":" in longname:
                p = pathlib.Path(longname)
                longname = p.resolve()
                longname = os.path.normpath(longname)
        shortname = get_short_path_name(longname)
        # print(f'{longname=}')
        # print(s,e,sta,end,endx)
        # print(f'{shortname=}')
        shortname = os.path.normpath(shortname)
        wholestringnew.append(wholestring[lastindi:s])
        wholestringnew.append(shortname)
        wholestringnew.append(endx)

        lastindi = e + end
        if ini == len(laazx) - 1:
            wholestringnew.append(wholestring[lastindi:])
        ini += 1
        kind = ""
        if os.path.ismount(shortname):
            kind = "mount"
        elif os.path.isfile(shortname):
            kind = "file"
        elif os.path.isdir(shortname):
            kind = "dir"
        elif os.path.islink(shortname):
            kind = "link"
        allres.append([s, e, longname, shortname, kind])
    return "".join(wholestringnew), wholestringnew, allres


def get_short_path_name(long_name):
    output_buf_size = 4096
    output_buf = ctypes.create_unicode_buffer(output_buf_size)
    _ = _GetShortPathNameW(long_name, output_buf, output_buf_size)
    return output_buf.value


def list2cmdline(*args, **kwargs):
    c = get_path_from_string(
        subprocess.list2cmdline_original(*args, **kwargs),
        minlen=subprocconfig.minlen,
        convert_to_abs_path=subprocconfig.convert_to_abs_path,
    )[0]
    # print(c)
    return c


def _execute_child(
    self,
    args,
    executable,
    preexec_fn,
    close_fds,
    pass_fds,
    cwd,
    env,
    startupinfo,
    creationflags,
    shell,
    p2cread,
    p2cwrite,
    c2pread,
    c2pwrite,
    errread,
    errwrite,
    unused_restore_signals,
    unused_gid,
    unused_gids,
    unused_uid,
    unused_umask,
    unused_start_new_session,
):
    """Execute program (MS Windows version)"""

    assert not pass_fds, "pass_fds not supported on Windows."

    if isinstance(args, str):
        args = get_path_from_string(
            args,
            minlen=subprocconfig.minlen,
            convert_to_abs_path=subprocconfig.convert_to_abs_path,
        )[0]
        # print(args)
    elif isinstance(args, bytes):
        if shell:
            raise TypeError("bytes args is not allowed on Windows")
        args = list2cmdline([args])
    elif isinstance(args, os.PathLike):
        if shell:
            raise TypeError("path-like args is not allowed when " "shell is true")
        args = list2cmdline([args])
    else:
        args = list2cmdline(args)

    if executable is not None:
        executable = os.fsdecode(executable)

    # Process startup details
    if startupinfo is None:
        startupinfo = subprocess.STARTUPINFO()
    else:
        # bpo-34044: Copy STARTUPINFO since it is modified above,
        # so the caller can reuse it multiple times.
        startupinfo = startupinfo.copy()

    use_std_handles = -1 not in (p2cread, c2pwrite, errwrite)
    if use_std_handles:
        startupinfo.dwFlags |= _winapi.STARTF_USESTDHANDLES
        startupinfo.hStdInput = p2cread
        startupinfo.hStdOutput = c2pwrite
        startupinfo.hStdError = errwrite

    attribute_list = startupinfo.lpAttributeList
    have_handle_list = bool(
        attribute_list
        and "handle_list" in attribute_list
        and attribute_list["handle_list"]
    )

    # If we were given an handle_list or need to create one
    if have_handle_list or (use_std_handles and close_fds):
        if attribute_list is None:
            attribute_list = startupinfo.lpAttributeList = {}
        handle_list = attribute_list["handle_list"] = list(
            attribute_list.get("handle_list", [])
        )

        if use_std_handles:
            handle_list += [int(p2cread), int(c2pwrite), int(errwrite)]

        handle_list[:] = self._filter_handle_list(handle_list)

        if handle_list:
            if not close_fds:
                warnings.warn(
                    "startupinfo.lpAttributeList['handle_list'] "
                    "overriding close_fds",
                    RuntimeWarning,
                )

            # When using the handle_list we always request to inherit
            # handles but the only handles that will be inherited are
            # the ones in the handle_list
            close_fds = False

    if shell:
        startupinfo.dwFlags |= _winapi.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = _winapi.SW_HIDE
        if not executable:
            # gh-101283: without a fully-qualified path, before Windows
            # checks the system directories, it first looks in the
            # application directory, and also the current directory if
            # NeedCurrentDirectoryForExePathW(ExeName) is true, so try
            # to avoid executing unqualified "cmd.exe".
            comspec = os.environ.get("ComSpec")
            if not comspec:
                system_root = os.environ.get("SystemRoot", "")
                comspec = os.path.join(system_root, "System32", "cmd.exe")
                if not os.path.isabs(comspec):
                    raise FileNotFoundError(
                        "shell not found: neither %ComSpec% nor %SystemRoot% is set"
                    )
            if os.path.isabs(comspec):
                executable = comspec
        else:
            comspec = executable

        args = '{} /c "{}"'.format(comspec, args)

    if cwd is not None:
        cwd = os.fsdecode(cwd)

    sys.audit("subprocess.Popen", executable, args, cwd, env)

    # Start the process
    try:
        hp, ht, pid, tid = _winapi.CreateProcess(
            executable,
            args,
            # no special security
            None,
            None,
            int(not close_fds),
            creationflags,
            env,
            cwd,
            startupinfo,
        )
    finally:
        # Child is launched. Close the parent's copy of those pipe
        # handles that only the child should have open.  You need
        # to make sure that no handles to the write end of the
        # output pipe are maintained in this process or else the
        # pipe will not close when the child process exits and the
        # ReadFile will hang.
        self._close_pipe_fds(p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite)

    # Retain the process handle, but close the thread handle
    self._child_created = True
    self._handle = subprocess.Handle(hp)
    self.pid = pid
    _winapi.CloseHandle(ht)


def patch_subprocess():
    r"""
    Apply the subprocess patch for enhanced path conversion and execution on Windows.
    """
    if "win" in platform.system().lower():
        subprocess.list2cmdline_original = pickle.loads(
            pickle.dumps(subprocess.list2cmdline)
        )
        subprocess.list2cmdline = list2cmdline
        subprocess.Popen._execute_child = _execute_child

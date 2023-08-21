import os
import logging
import click
import webbrowser
import http.server
import socketserver


from ciocore import (
    loggeria,
    config,
    api_client,
    package_query,
)

from ciocore import __version__ as VERSION

from ciocore.uploader import Uploader
from ciocore.downloader import Downloader

logger = logging.getLogger("conductor cli")

LOG_LEVEL_HELP = """The logging level to display"""

LOG_DIR_HELP = """
Write a log file to the given directory. The log rotates, creating a new log file every day, while
storing logs for the last 7 days. The log file is named conductor_ul.log
"""

THREADS_HELP = """The number of threads that should download simultaneously"""

UPLOADER_DATABASE_FILEPATH_HELP = (
    "Specify a filepath to the local md5 caching database."
)
LOCATION_HELP = """
Specify a location tag to associate with uploads, downloads, and submissions. A location tag allows
you to limit the scope of your uploads and downloads to jobs sharing the same location tag. This is
useful while using the uploader or downloader in daemon mode.
"""
UPLOADER_MD5_CACHING_HELP = """
Use cached md5s. This can dramatically improve the uploading times, as md5 checking can be very
time consuming. Caching md5s allows subsequent uploads (of the same files) to skip the md5
generation process (if the files appear to not have been modified since the last time they were
submitted). The cache is stored locally and uses a file's modification time and file size to
intelligently guess whether the file has changed. Set this flag to False if there is concern that
files may not be getting re-uploaded properly
"""

UPLOADER_PATHS_HELP = """
A list of paths to upload. Use quotes if paths contain spaces or special characters"""

DOWNLOADER_JOB_ID_HELP = """
The job id(s) to download. When specified will only download those jobs and terminate afterwards
"""

DOWNLOADER_DEST_HELP = """
Override the output directory"""

PACKAGES_FORMAT_OPTIONS = ["text", "markdown", "html"]
PACKAGES_FORMAT_HELP = """
text: The output is a simple list of software names and versions, with nesting to indicate plugin
compatibility. Output is sent to stdout.

markdown: Designed for use in other markdown documentation systems where it benefits from consistent
styling. Output is sent to stdout and can be piped to a file.

html: Opens a browser window and displays the output in a simple html page.
"""

DOCS_PORT_HELP = """
The port to serve the documentation on. Defaults to 8025.
"""
DEFAULT_DOCS_PORT=8025

LOG_FORMATTER = logging.Formatter(
    "%(asctime)s  %(name)s%(levelname)9s  %(threadName)s:  %(message)s"
)


cfg = config.get()
DEFAULT_CONFIG_MD5_CACHING = cfg["md5_caching"]
DEFAULT_CONFIG_THREAD_COUNT = cfg["thread_count"]
DEFAULT_CONFIG_LOG_LEVEL = cfg["log_level"]

def _set_logging(log_level=None, log_filepath=None):
    level = loggeria.LEVEL_MAP.get(log_level)
    loggeria.setup_conductor_logging(
        logger_level=level,
        console_formatter=LOG_FORMATTER,
        file_formatter=LOG_FORMATTER,
        log_filepath=log_filepath,
    )

def _register(client):
    api_client.ApiClient.register_client(
        client_name=client.CLIENT_NAME, client_version=VERSION
    )

########################### MAIN #################################
@click.group(invoke_without_command=True)
@click.pass_context
@click.option('-v', '--version', is_flag=True, help='Print the version and exit.')
def main(ctx, version):
    """Conductor Command-line interface."""
    if not ctx.invoked_subcommand:
        if version:
            click.echo(VERSION)
            ctx.exit()
        click.echo(ctx.get_help())
        ctx.exit()

############################# UPLOADER #############################
@main.command()
@click.option("-db", "--database_filepath", help=UPLOADER_DATABASE_FILEPATH_HELP)
@click.option( "-md5", "--md5_caching", help=UPLOADER_MD5_CACHING_HELP, type=bool, default=DEFAULT_CONFIG_MD5_CACHING,)
@click.option("-lv", "--log_level", help=LOG_LEVEL_HELP, type=click.Choice(choices=loggeria.LEVELS, case_sensitive=False), show_choices=True, default=DEFAULT_CONFIG_LOG_LEVEL)
@click.option("-ld", "--log_dir", help=LOG_DIR_HELP)
@click.option("-tc", "--thread_count", type=int, help=THREADS_HELP, default=DEFAULT_CONFIG_THREAD_COUNT)
@click.option("-lc", "--location", help=LOCATION_HELP)
@click.argument("paths", nargs=-1, type=click.Path(exists=True, resolve_path=True))
def upload(
    database_filepath, location, md5_caching, log_level, log_dir, thread_count, paths
):
    """Upload files to Conductor.
    
    With no arguments, the uploader runs in daemon mode, watching for files to upload for submitted
    jobs.

    Alternatively, specify a list of paths to upload.
    
    Example:
    conductor upload file1 file2 file3
    """
    logfile = log_dir and os.path.join(log_dir, "conductor_ul.log")
    _set_logging(log_level, logfile)

    args_dict = {
        "database_filepath": database_filepath,
        "location": location,
        "md5_caching": md5_caching,
        "log_level": log_level,
        "log_dir": log_dir,
        "thread_count": thread_count,
    }

    up = Uploader(args_dict)

    if paths:
        up.assets_only(*paths)
        return

    up.main()

########################### DOWNLOADER #############################
@main.command()
@click.argument("jobids", nargs=-1)
@click.option("-d", "--destination", help=DOWNLOADER_DEST_HELP)
@click.option("-lv", "--log_level", help=LOG_LEVEL_HELP, type=click.Choice(choices=loggeria.LEVELS, case_sensitive=False), show_choices=True, default=DEFAULT_CONFIG_LOG_LEVEL)
@click.option("-ld", "--log_dir", help=LOG_DIR_HELP)
@click.option("-tc", "--thread_count", type=int, help=THREADS_HELP, default=DEFAULT_CONFIG_THREAD_COUNT)
@click.option("-lc", "--location", help=LOCATION_HELP)

def download(jobids, destination, location, log_level, log_dir, thread_count):
    """
    Download renders and other output files from Conductor. You can give a list of job ids to
    download, or you can omit jobids and the downloader will run in daemon mode.

    If you provide jobids, the default behavior is to download all the files from completed tasks
    for those jobs. You can however specify an explicit set of tasks to downloade by providing a
    task range spec after each job id. To do so, append a colon to the job id and then a compact
    task specification. See the examples.

    In daemon mode, the downloader polls for new jobs to download. You can specify a location tag to
    limit the scope of the downloader to only download jobs that were submitted with the same
    location tag.

    Examples:
    conductor download # daemon mode
    conductor download 1234 1235
    conductor download 1234:1-10
    conductor download 1234:1-5x2,10,12-14
    conductor download 1234:1-5 1235:5-10
    """
    logfile = log_dir and os.path.join(log_dir, "conductor_dl.log")
    _set_logging(log_level, logfile)
    _register(Downloader)
    if jobids:
        Downloader.download_jobs(
            jobids,
            thread_count=thread_count,
            output_dir=destination,
        )
    else:
        Downloader.start_daemon(
            thread_count=thread_count, location=location, output_dir=destination
        )


########################### PACKAGES #############################
@main.command()
@click.option(
    "-f",
    "--fmt",
    "--format",
    default="text",
    help=PACKAGES_FORMAT_HELP,
    type=click.Choice(choices=PACKAGES_FORMAT_OPTIONS, case_sensitive=False),
)
def packages(fmt):
    """List the softweare packages available on the render nodes in the cloud."""
    package_query.pq(format=fmt)


########################### DOCS #############################
@main.command()
@click.option(
    "-p",
    "--port",
    help=DOCS_PORT_HELP,
    type=int,
    default=DEFAULT_DOCS_PORT,
)
def docs(port):
    """Open the Conductor Core documentation in a web browser."""
    
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
 
        print(f"Server started at http://localhost:{port}")
        print("Press Ctrl+C to stop the server")
        
        # Change to the directory containing your site
        current_dir =  os.path.dirname(os.path.abspath(__file__))
        site_dir = os.path.join(current_dir, "docsite")
        os.chdir(site_dir)
        
        # Start the server
        localhost_url = f"http://localhost:{port}"
        webbrowser.open(localhost_url)
        httpd.serve_forever()


########################### DEPRECATIONS #############################
############################# UPLOADER #############################
DEPRECATED_PATHS_HELP="Specify a list of paths to upload."

@main.command(deprecated=True)
@click.option("-db", "--database_filepath", help=UPLOADER_DATABASE_FILEPATH_HELP)
@click.option( "-md5", "--md5_caching", help=UPLOADER_MD5_CACHING_HELP, type=bool, default=DEFAULT_CONFIG_MD5_CACHING   )
@click.option("-lv", "--log_level", help=LOG_LEVEL_HELP, type=click.Choice(choices=loggeria.LEVELS, case_sensitive=False), show_choices=True, default=DEFAULT_CONFIG_LOG_LEVEL)
@click.option("-ld", "--log_dir", help=LOG_DIR_HELP)
@click.option("-tc", "--thread_count", type=int, help=THREADS_HELP, default=DEFAULT_CONFIG_THREAD_COUNT)
@click.option("-lc", "--location", help=LOCATION_HELP)
@click.option("-p", "--paths", help=DEPRECATED_PATHS_HELP, multiple=True, type=click.Path(exists=True, resolve_path=True))



def uploader(
    database_filepath, location, md5_caching, log_level, log_dir, thread_count, paths
):
    """Upload files to Conductor.

    With no arguments, the uploader runs in daemon mode, watching for files to upload for submitted
    jobs.

    Alternatively, specify a list of paths to upload with the --paths option.
    
    Example:
    conductor upload file1 file2 file3
    """
    logfile = log_dir and os.path.join(log_dir, "conductor_ul.log")
    _set_logging(log_level, logfile)

    args_dict = {
        "database_filepath": database_filepath,
        "location": location,
        "md5_caching": md5_caching,
        "log_level": log_level,
        "log_dir": log_dir,
        "thread_count": thread_count,
    }

    up = Uploader(args_dict)

    if paths:
        up.assets_only(*paths)
        return

    up.main()

########################### DOWNLOADER #############################
DEPRECATED_JOBID_HELP="Download all the files from completed tasks for the given jobs."
DEPRECATED_TASKID_HELP="Download the files from the given tasks in the specified job."

@main.command(deprecated=True)
@click.option("-o", "--output", help=DOWNLOADER_DEST_HELP)
@click.option("-j", "--job_id", help=DEPRECATED_JOBID_HELP)
@click.option("-t", "--task_id", help=DEPRECATED_TASKID_HELP)
@click.option("-lv", "--log_level", help=LOG_LEVEL_HELP, type=click.Choice(choices=loggeria.LEVELS, case_sensitive=False), show_choices=True, default=DEFAULT_CONFIG_LOG_LEVEL)
@click.option("-ld", "--log_dir", help=LOG_DIR_HELP)
@click.option("-tc", "--thread_count", type=int, help=THREADS_HELP, default=DEFAULT_CONFIG_THREAD_COUNT)
@click.option("-lc", "--location", help=LOCATION_HELP)
@click.pass_context
def downloader(ctx, job_id, task_id, output, location, log_level, log_dir, thread_count):
    """
    Download renders and other output files from Conductor. You can specify a job id and optional task id to
    download, or you can omit all options and the downloader will run in daemon mode.
    
    In daemon mode, the downloader polls for new jobs to download. You can specify a location tag to
    limit the scope of the downloader to only download jobs that were submitted with the same
    location tag.

    Examples:
    conductor downloader # daemon mode
    conductor downloader --job_id --task_id 01234 
    conductor downloader --task_id --task_id 123
    """
    
    logfile = log_dir and os.path.join(log_dir, "conductor_dl.log")
    _set_logging(log_level, logfile)
    _register(Downloader)
    
    if not job_id and not task_id:
        Downloader.start_daemon(
            thread_count=thread_count, location=location, output_dir=output
        )
        ctx.exit(0)
    
    if task_id:
         job_id = job_id + ":" + task_id

    Downloader.download_jobs(
        (job_id,),
        thread_count=thread_count,
        output_dir=output,
    )

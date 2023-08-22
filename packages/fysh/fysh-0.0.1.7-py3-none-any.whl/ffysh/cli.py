import click
from .modules.internals import project, authorization
from . import Stream, Dataset
from refyre.cluster import FileCluster

@click.group()
def ffysh():
    pass


@ffysh.command()
def init():
    project.init_project()


@ffysh.command()
def login():
    authorization.login()


@ffysh.command()
@click.option('-d', '--dataset', help='Enter dataset ID which can be located in a dataset\'s URL.', required=True)
def download(dataset):
    """Downloads an entire dataset."""
    try:
        stream = Dataset(dataset_id=dataset).create_stream()
    except:
        click.echo("Dataset either is private or does not exist.")
        return
    stream.download(whole=True)


@ffysh.command()
@click.option('-d', '--dataset', help='Enter dataset ID which can be located in a dataset\'s URL.', required=True)
@click.option('-b', '--batch', type=int, help='Specifies the number of files to be downloaded. Starts off where specified stream ended or first file if stream is not specified', required=True)
@click.option('-c', '--chunk', type=int, help='The number of filed stored locally is equivalent to the chunk size plus the batch size.', required=True)
@click.option('-s', '--stream', help='Enter stream ID to continue chunking from a previous session.', required=False)
@click.option('-np', '--nopredownload', is_flag=True, help="Blocks downloading multiple files at once when iterating through the stream.")
@click.option('-r', '--reset', is_flag=True, help="Deletes all files (previous chunks) in saved stream directory")
@click.option('-ns', '--nosave', is_flag=True, help='Does not save stream to a directory. Assets can be found in the assets folder of the project directory.')
def load(dataset, batch, chunk, stream, nopredownload=False, reset=False, nosave=False):
    dataset_id = dataset
    batch_size = batch
    chunk_size = chunk
    stream_id = stream
    save = not nosave
    predownload = not nopredownload
    """Loads the next batch of a dataset."""
    if not isinstance(batch_size, int):
        raise AssertionError("Batch size must be an integer.")
    if batch_size <= 0:
        raise AssertionError("Batch size must be greater than 0.")
    if not isinstance(chunk_size, int):
        raise AssertionError("Chunk size must be an integer.")
    if chunk_size <= 0:
        raise AssertionError("Chunk size must be greater than 0.")

    try:
        dataset = Dataset(dataset_id=dataset_id)
    except:
        click.echo("Dataset either is private or does not exist.")
        return

    if stream is not None:
        try: 
            stream = Stream.load(saved_stream_id=stream_id)
        except:
            click.echo("Stream does not exist.")
            return
        if stream.dataset_id != dataset_id:
            click.echo(f"Stream belongs to incorrect dataset. Stream belongs to dataset {stream.dataset_id} while dataset {dataset_id} was specified.")
            return
        it = stream.create_iterator(start_index=stream._iterator_start_index, chunk_size=chunk_size, pre_download=predownload, batch_size=batch_size, save=save, reset=reset)
    else:
        stream = dataset.create_stream()
        click.echo(f"Created stream {stream.stream_id}. Use this stream ID to continue chunking from a previous session.")
        it = stream.create_iterator(start_index=0, chunk_size=chunk_size, pre_download=predownload, batch_size=batch_size, save=save, reset=reset)

    try:
        next(it)
    except StopIteration:
        click.echo("Stream already finished.")
        return

@ffysh.command()
@click.option('-f', '--folder', help='Enter the folder which will be the base dataset', required=True)
@click.option('-n', '--name', help='Enter the name of the dataset', required=True)
@click.option('-d', '--description', help='Enter the description of the dataset', required=True)
def create(folder, name, description):
    Dataset.new(folder, name, description)

@ffysh.command()
@click.option('-d', '--dataset', help='Enter dataset ID which can be located in a dataset\'s URL.', required=True)
@click.option('-f', '--dir', help='Enter the folder which contains all the files', required=True)
@click.option('-n', '--filenames', help='Enter the filenames pattern.', required=True)
def add(dataset, dir, filenames):
    
    dataset = Dataset(dataset)
    files = FileCluster(input_paths = [dir], input_patterns = [f'g!{filenames}'])

    print('Starting to add files ...')

    for file in files.vals():
        dataset.add_assets(str(file))

    print('All files added in!')


@ffysh.command()
@click.option('-d', '--dataset', help='Enter dataset ID which can be located in a dataset\'s URL.', required=True)
@click.option('-t', '--title', help='Enter the title of the Pull Request', required=True)
@click.option('-m', '--message', help='Enter the message of the Pull Request', required=True)
@click.option('-f', '--dir', help='Enter the folder which contains all the files', required=True)
@click.option('-n', '--filenames', help='Enter the filenames pattern.', required=True)
def pr_create(dataset, title, message, dir, filenames):

    dataset = Dataset(dataset)
    
    pr = dataset.create_pr(title, message)["data"]
    
    print(pr)
    files = FileCluster(input_paths = [dir], input_patterns = [f'g!{filenames}'])

    print('Starting to add files ...')

    dataset.add_to_pr(pr["_id"], [str(f) for f in files])

    print('All files sucessfully added.')
    print("List:")
    print('\n'.join([str(f) for f in files]))


@ffysh.command()
@click.option('-d', '--dataset', help='Enter dataset ID which can be located in a dataset\'s URL.', required=True)
@click.option('-p', '--pr', help='Enter pull request ID which can be located in a pr\'s URL.', required=True)
@click.option('-f', '--dir', help='Enter the folder which contains all the files', required=True)
@click.option('-n', '--filenames', help='Enter the filenames pattern.', required=True)
def pr_add(dataset, pr, dir, filenames):
    dataset = Dataset(dataset)
    
    files = FileCluster(input_paths = [dir], input_patterns = [f'g!{filenames}'])

    print('Starting to add files ...')

    dataset.add_to_pr(pr, [str(f) for f in files])

    print('All files sucessfully added.')
    print("List:")
    print('\n'.join([str(f) for f in files]))
    



def main():
    ffysh()

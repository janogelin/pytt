import os
import tempfile
import pyarrow.parquet as pq
import pandas as pd
import pytest
from unittest import mock
import web.crawler as crawler
from multiprocessing.dummy import Pool as ThreadPool

# Helper to write a temp URI file
def write_uri_file(uris):
    fd, path = tempfile.mkstemp(suffix='.txt')
    with os.fdopen(fd, 'w') as f:
        for uri in uris:
            f.write(uri + '\n')
    return path

def read_parquet(path):
    table = pq.read_table(path)
    return table.to_pandas()

@mock.patch('web.crawler.requests.get')
def test_crawl_success(mock_get):
    # Mock two URLs
    mock_get.side_effect = [
        mock.Mock(status_code=200, content=b'hello', ok=True, text='hello world'),
        mock.Mock(status_code=404, content=b'', ok=False, text=''),
    ]
    uris = ['http://test1', 'http://test2']
    out_file = tempfile.mktemp(suffix='.parquet')
    try:
        crawler.crawl(uris, out_file, pool_cls=ThreadPool, fetch_fn=crawler.fetch_url, pool_size=2)
        df = read_parquet(out_file)
        assert set(df['url']) == set(uris)
        assert 200 in df['status_code'].values
        assert 404 in df['status_code'].values or None in df['status_code'].values
    finally:
        if os.path.exists(out_file):
            os.remove(out_file)

@mock.patch('web.crawler.requests.get')
def test_crawl_empty_file(mock_get):
    uris = []
    out_file = tempfile.mktemp(suffix='.parquet')
    with pytest.raises(SystemExit):
        crawler.crawl(uris, out_file, pool_cls=ThreadPool, fetch_fn=crawler.fetch_url, pool_size=2)
    if os.path.exists(out_file):
        os.remove(out_file)

@mock.patch('web.crawler.requests.get')
def test_crawl_invalid_url(mock_get):
    # Simulate request exception
    mock_get.side_effect = Exception('Connection error')
    uris = ['http://badurl']
    out_file = tempfile.mktemp(suffix='.parquet')
    try:
        crawler.crawl(uris, out_file, pool_cls=ThreadPool, fetch_fn=crawler.fetch_url, pool_size=1)
        df = read_parquet(out_file)
        assert df.iloc[0]['status_code'] is None
        assert 'ERROR' in df.iloc[0]['snippet']
    finally:
        if os.path.exists(out_file):
            os.remove(out_file) 
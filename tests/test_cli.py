from stardust.cli import main


def test_main_with_custom_arguments(monkeypatch):
    from argparse import Namespace
    from unittest.mock import patch

    mock_args = Namespace(file='custom_app.py', port=8080, host='127.0.0.1', log_level='info', debug=True)
    monkeypatch.setattr('argparse.ArgumentParser.parse_args', lambda self: mock_args)

    with patch('stardust.cli.handle', return_value='mock_function') as mock_handle, \
         patch('stardust.cli.Stardust') as mock_stardust, \
         patch('uvicorn.run') as mock_uvicorn_run:

        main()

        mock_handle.assert_called_once_with('custom_app.py')
        mock_stardust.assert_called_once_with(fun='mock_function', port=8080, debug=True)
        mock_uvicorn_run.assert_called_once_with(
            mock_stardust().build(),
            host='127.0.0.1',
            port=8080,
            access_log=True,
            log_level='info',
        )

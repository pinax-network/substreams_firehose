"""
SPDX-License-Identifier: MIT

Entry point for the config GUI application.
"""

import logging

from pyfirehose.config.ui.app import ConfigApp

if __name__ == '__main__':
    logging.basicConfig(
        handlers=[logging.FileHandler('logs/config.log', mode='w')],
        level=logging.INFO,
        format='%(asctime)s:T+%(relativeCreated)d %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        force=True
    )

    logging.addLevelName(logging.DEBUG, '[DEBUG]')
    logging.addLevelName(logging.INFO, '[*]')
    logging.addLevelName(logging.WARNING, '[!]')
    logging.addLevelName(logging.ERROR, '[ERROR]')
    logging.addLevelName(logging.CRITICAL, '[CRITICAL]')

    APP = ConfigApp().run()

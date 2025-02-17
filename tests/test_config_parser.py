__author__ = "Mandar Patil (mandarons@pm.me)"

import os
import unittest
import shutil

from src import (
    DEFAULT_RETRY_LOGIN_INTERVAL_SEC,
    config_parser,
    DEFAULT_DRIVE_DESTINATION,
    DEFAULT_PHOTOS_DESTINATION,
    DEFAULT_ROOT_DESTINATION,
    DEFAULT_SYNC_INTERVAL_SEC,
    read_config,
)
import tests


class TestConfigParser(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_read_config_default_config_path(self):
        # Default config path
        self.assertIsNotNone(read_config(config_path=tests.CONFIG_PATH))

    def test_read_config_overridden_config_path(self):
        # Overridden config path
        self.assertIsNotNone(read_config(config_path=tests.CONFIG_PATH))

    def test_read_config_invalid_config_path(self):
        # Invalid config path
        self.assertIsNone(read_config(config_path="invalid/path"))

    def test_read_config_none_config_path(self):
        # None config path
        self.assertIsNone(read_config(config_path=None))

    def test_get_drive_sync_interval(self):
        # Given sync interval
        config = read_config(config_path=tests.CONFIG_PATH)
        self.assertEqual(
            config["drive"]["sync_interval"],
            config_parser.get_drive_sync_interval(config=config),
        )

    def test_get_drive_sync_interval_default(self):
        # Default sync interval
        config = read_config(config_path=tests.CONFIG_PATH)
        del config["drive"]["sync_interval"]
        self.assertEqual(
            DEFAULT_SYNC_INTERVAL_SEC,
            config_parser.get_drive_sync_interval(config=config),
        )

    def test_get_drive_sync_interval_none_config(self):
        # None config
        self.assertEqual(
            DEFAULT_SYNC_INTERVAL_SEC,
            config_parser.get_drive_sync_interval(config=None),
        )

    def test_get_retry_login_interval(self):
        # Given  interval
        config = read_config(config_path=tests.CONFIG_PATH)
        self.assertEqual(
            config["app"]["credentials"]["retry_login_interval"],
            config_parser.get_retry_login_interval(config=config),
        )

    def test_get_retry_login_interval_default(self):
        # Default interval
        config = read_config(config_path=tests.CONFIG_PATH)
        del (config["app"]["credentials"]["retry_login_interval"],)
        self.assertEqual(
            DEFAULT_RETRY_LOGIN_INTERVAL_SEC,
            config_parser.get_retry_login_interval(config=config),
        )

    def test_get_retry_login_interval_none_config(self):
        # None config
        self.assertEqual(
            DEFAULT_RETRY_LOGIN_INTERVAL_SEC,
            config_parser.get_retry_login_interval(config=None),
        )

    def test_get_photos_sync_interval(self):
        # Given sync interval
        config = read_config(config_path=tests.CONFIG_PATH)
        self.assertEqual(
            config["photos"]["sync_interval"],
            config_parser.get_photos_sync_interval(config=config),
        )

    def test_get_photos_sync_interval_default(self):
        # Default sync interval
        config = read_config(config_path=tests.CONFIG_PATH)
        del config["photos"]["sync_interval"]
        self.assertEqual(
            DEFAULT_SYNC_INTERVAL_SEC,
            config_parser.get_photos_sync_interval(config=config),
        )

    def test_get_photos_sync_interval_none_config(self):
        # None config
        self.assertEqual(
            DEFAULT_SYNC_INTERVAL_SEC,
            config_parser.get_photos_sync_interval(config=None),
        )

    def test_prepare_drive_destination_given(self):
        config = read_config(config_path=tests.CONFIG_PATH)
        # Given destination
        actual = config_parser.prepare_drive_destination(config=config)
        self.assertEqual(
            os.path.abspath(
                os.path.join(config["app"]["root"], config["drive"]["destination"])
            ),
            actual,
        )
        self.assertTrue(os.path.exists(actual))
        self.assertTrue(os.path.isdir(actual))
        os.rmdir(actual)

    def test_prepare_drive_destination_default(self):
        config = read_config(config_path=tests.CONFIG_PATH)
        # Default destination
        del config["drive"]["destination"]
        actual = config_parser.prepare_drive_destination(config=config)
        self.assertEqual(
            os.path.abspath(
                os.path.join(
                    DEFAULT_ROOT_DESTINATION,
                    DEFAULT_DRIVE_DESTINATION,
                )
            ),
            actual,
        )
        self.assertTrue(os.path.exists(actual))
        self.assertTrue(os.path.isdir(actual))
        os.rmdir(actual)

    def test_prepare_drive_destination_none_config(self):
        # None config
        actual = config_parser.prepare_drive_destination(config=None)
        self.assertEqual(
            os.path.abspath(
                os.path.join(
                    DEFAULT_ROOT_DESTINATION,
                    DEFAULT_DRIVE_DESTINATION,
                )
            ),
            actual,
        )
        self.assertTrue(os.path.exists(actual))
        self.assertTrue(os.path.isdir(actual))
        os.rmdir(actual)

    def test_get_username_given(self):
        config = read_config(config_path=tests.CONFIG_PATH)
        # Given username
        self.assertEqual(
            config["app"]["credentials"]["username"],
            config_parser.get_username(config=config),
        )

    def test_get_username_none_config(self):
        # None config
        self.assertIsNone(config_parser.get_username(config=None))

    def test_get_username_empty(self):
        # Empty username
        config = read_config(config_path=tests.CONFIG_PATH)
        config["app"]["credentials"]["username"] = ""
        self.assertIsNone(config_parser.get_username(config=config))

    def test_get_remove_obsolete(self):
        config = read_config(config_path=tests.CONFIG_PATH)
        config["drive"]["remove_obsolete"] = True
        self.assertTrue(config_parser.get_drive_remove_obsolete(config=config))
        del config["drive"]["remove_obsolete"]
        self.assertFalse(config_parser.get_drive_remove_obsolete(config=config))

    def test_get_remove_obsolete_none_config(self):
        self.assertFalse(config_parser.get_drive_remove_obsolete(config=None))

    def test_get_smtp_no_tls(self):
        config = {"app": {"smtp": {"no_tls": True}}}
        self.assertTrue(config_parser.get_smtp_no_tls(config=config))

    def test_get_smtp_tls(self):
        config = {"app": {"smtp": {"no_tls": False}}}
        self.assertFalse(config_parser.get_smtp_no_tls(config=config))

    def test_get_smtp_empty(self):
        config = {"app": {"smtp": {}}}
        self.assertFalse(config_parser.get_smtp_no_tls(config=config))

    def test_get_smtp_email(self):
        # Given email
        config = {"app": {"smtp": {"email": "user@test.com"}}}
        self.assertEqual(
            config["app"]["smtp"]["email"], config_parser.get_smtp_email(config=config)
        )

    def test_smtp_email_none_config(self):
        self.assertIsNone(config_parser.get_smtp_email(config=None))

    def test_get_smtp_to_email(self):
        # Given email
        config = {"app": {"smtp": {"to": "receiver@test.com"}}}
        self.assertEqual(
            config["app"]["smtp"]["to"], config_parser.get_smtp_to_email(config=config)
        )

    def test_get_smtp_to_email_default(self):
        # Given email
        config = {"app": {"smtp": {"email": "from@test.com"}}}
        self.assertEqual(
            config["app"]["smtp"]["email"],
            config_parser.get_smtp_to_email(config=config),
        )

    def test_smtp_to_email_none_config(self):
        self.assertIsNone(config_parser.get_smtp_to_email(config=None))

    def test_get_smtp_host(self):
        # Given host
        config = {"app": {"smtp": {"host": "smtp.test.com"}}}
        self.assertEqual(
            config["app"]["smtp"]["host"], config_parser.get_smtp_host(config=config)
        )

    def test_smtp_host_none_config(self):
        self.assertIsNone(config_parser.get_smtp_host(config=None))

    def test_get_smtp_port(self):
        # Given port
        config = {"app": {"smtp": {"port": 587}}}
        self.assertEqual(
            config["app"]["smtp"]["port"], config_parser.get_smtp_port(config=config)
        )

    def test_smtp_port_none_config(self):
        self.assertIsNone(config_parser.get_smtp_port(config=None))

    def test_get_smtp_password(self):
        # Given password
        config = {"app": {"smtp": {"password": "password"}}}
        self.assertEqual(
            config["app"]["smtp"]["password"],
            config_parser.get_smtp_password(config=config),
        )

    def test_smtp_password_none_config(self):
        self.assertIsNone(config_parser.get_smtp_password(config=None))

    def test_prepare_photos_destination(self):
        config = read_config(config_path=tests.CONFIG_PATH)
        # Given destination
        actual = config_parser.prepare_photos_destination(config=config)
        self.assertEqual(
            os.path.abspath(
                os.path.join(config["app"]["root"], config["photos"]["destination"])
            ),
            actual,
        )
        self.assertTrue(os.path.exists(actual))
        self.assertTrue(os.path.isdir(actual))
        os.rmdir(actual)

    def test_prepare_photos_destination_default(self):
        config = read_config(config_path=tests.CONFIG_PATH)
        # Default destination
        del config["photos"]["destination"]
        actual = config_parser.prepare_photos_destination(config=config)
        self.assertEqual(
            os.path.abspath(
                os.path.join(
                    DEFAULT_ROOT_DESTINATION,
                    DEFAULT_PHOTOS_DESTINATION,
                )
            ),
            actual,
        )
        self.assertTrue(os.path.exists(actual))
        self.assertTrue(os.path.isdir(actual))
        shutil.rmtree(actual)

    def test_prepare_photos_destination_none_config(self):
        # None config
        actual = config_parser.prepare_photos_destination(config=None)
        self.assertEqual(
            os.path.abspath(
                os.path.join(
                    DEFAULT_ROOT_DESTINATION,
                    DEFAULT_PHOTOS_DESTINATION,
                )
            ),
            actual,
        )
        self.assertTrue(os.path.exists(actual))
        self.assertTrue(os.path.isdir(actual))
        shutil.rmtree(actual)

    def test_get_photos_remove_obsolete(self):
        config = read_config(config_path=tests.CONFIG_PATH)
        config["photos"]["remove_obsolete"] = True
        self.assertTrue(config_parser.get_photos_remove_obsolete(config=config))

    def test_get_photos_remove_obsolete_missing(self):
        config = read_config(config_path=tests.CONFIG_PATH)
        del config["photos"]["remove_obsolete"]
        self.assertFalse(config_parser.get_photos_remove_obsolete(config=config))

    def test_get_photos_remove_obsolete_none_config(self):
        self.assertFalse(config_parser.get_photos_remove_obsolete(config=None))

    def test_get_photos_filters(self):
        config = read_config(config_path=tests.CONFIG_PATH)
        expected_albums = ["Screenshots", "Selfies"]
        expected_file_sizes = ["original", "medium", "thumb"]
        config["photos"]["filters"]["albums"] = expected_albums
        config["photos"]["filters"]["file_sizes"] = expected_file_sizes
        actual = config_parser.get_photos_filters(config=config)
        self.assertIsNotNone(actual)
        self.assertListEqual(actual["albums"], expected_albums)
        self.assertListEqual(actual["file_sizes"], expected_file_sizes)

    def test_get_photos_filters_no_filters(self):
        config = read_config(config_path=tests.CONFIG_PATH)
        del config["photos"]["filters"]
        actual = config_parser.get_photos_filters(config=config)
        self.assertIsNone(actual["albums"])
        self.assertEqual(actual["file_sizes"][0], "original")

    def test_get_photos_filters_invalid_file_size(self):
        config = read_config(config_path=tests.CONFIG_PATH)
        config["photos"] = {"filters": {"file_sizes": ["invalid"]}}
        actual = config_parser.get_photos_filters(config=config)
        self.assertEqual(actual["file_sizes"][0], "original")

    def test_get_photos_filters_no_file_sizes(self):
        config = read_config(config_path=tests.CONFIG_PATH)
        del config["photos"]["filters"]["file_sizes"]
        actual = config_parser.get_photos_filters(config=config)
        self.assertEqual(actual["file_sizes"][0], "original")

    def test_get_region_default(self):
        config = read_config(config_path=tests.CONFIG_PATH)
        del config["app"]["region"]
        actual = config_parser.get_region(config=config)
        self.assertEqual(actual, "global")

    def test_get_region_default_if_invalid(self):
        config = read_config(config_path=tests.CONFIG_PATH)
        config["app"]["region"] = "invalid"
        actual = config_parser.get_region(config=config)
        self.assertEqual(actual, "global")

    def test_get_region_valid(self):
        config = read_config(config_path=tests.CONFIG_PATH)
        config["app"]["region"] = "china"
        actual = config_parser.get_region(config=config)
        self.assertEqual(actual, "china")

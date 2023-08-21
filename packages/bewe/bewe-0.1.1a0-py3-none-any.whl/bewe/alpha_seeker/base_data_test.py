import unittest

from bewe.alpha_seeker import base_data


class TestBaseData(unittest.TestCase):

    def get_mock_units(self):
        data_format = base_data.DataFormat(
            required_field=['open', 'close']
        )

        return [
            base_data.DataUnit(
                format=data_format,
                data={'open': 100, 'close': 50},
                actionable_price=80
            ),
            base_data.DataUnit(
                format=data_format,
                data={'open': 80, 'close': 100},
                actionable_price=80
            )
        ]

    def test_iter(self):
        asset_name = 'mock'
        mock_data = self.get_mock_units()
        container = base_data.DataContainer(asset_name, data=mock_data)
        iter_units = [unit for unit in container]
        self.assertEqual(len(iter_units), 2)
        self.assertListEqual(iter_units, mock_data)

    def test_empty_iter(self):
        asset_name = 'mock'
        container = base_data.DataContainer(asset_name)
        iter_units = [unit for unit in container]
        self.assertEqual(len(iter_units), 0)


if __name__ == '__main__':
    unittest.main()

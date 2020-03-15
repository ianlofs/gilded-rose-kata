def pytest_addoption(parser):
    parser.addoption(
        "--days",
        default="10",
        help="Number of days to run the test for",
    )
    parser.addoption(
        "--items",
        default="10",
        help="Number of items for sale at the Gilded Rose",
    )


def pytest_generate_tests(metafunc):
    if "num_days" in metafunc.fixturenames:
        metafunc.parametrize("num_days", (int(metafunc.config.getoption("days")),))

    if "num_items" in metafunc.fixturenames:
        metafunc.parametrize("num_items", (int(metafunc.config.getoption("items")),))

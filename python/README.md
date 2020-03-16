# Python Gilded Rose Kata

This is my submission for the Gilded Rose Kata. I followed the following procedure when refactoring the code and adding the requested feature.
1. Rename current update_quality function to update_quality_old and create a new function update_quality which just calls update_quality_old..
1. Added a test harness that compared the output of the update_quality_old to update_quality.
1. Rewrote update_quality trying to clarify the functions logic as much as possible while testing it against the output of the old function.
1. When I was confident that the update_qualify function replicated the logic of update_quality_old, I added the requested feature to update_quality and added tests for the logic described in the top level readme.
1. Further refactored to reduce the complexity of update_quality's conditional logic.


### Runtime requirements
These must be installed in order to setup the testing environment.

* python >= 3.6
* [pipenv](https://pipenv-fork.readthedocs.io/en/latest/)


### Setup testing environment
`$ pipenv install --dev`


### Test runner
This uses [pytest](https://docs.pytest.org/en/latest/) to run and gather the results of the tests. There are two custom options for the test:
* `--days=DAYS           Number of days to run the test for.`
* `--items=ITEMS         Number of items for sale at the Gilded Rose`.

To run the tests,

`$ pytest test_guilded_rose --days=10 --items=10`

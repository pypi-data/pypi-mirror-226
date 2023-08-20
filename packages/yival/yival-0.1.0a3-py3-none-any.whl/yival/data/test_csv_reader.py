import logging

from ..schemas.common_structures import InputData
from ..schemas.reader_configs import CSVReaderConfig
from .csv_reader import CSVReader


def test_basic_csv_reading(tmp_path):
    csv_content = """input
input1
input2
input3"""
    csv_file = tmp_path / "basic.csv"
    csv_file.write_text(csv_content)

    config = CSVReaderConfig()  # Default configuration
    reader = CSVReader(config)
    results = list(reader.read(csv_file))

    assert len(results) == 1
    assert len(results[0]) == 3
    assert isinstance(results[0][0], InputData)
    assert results[0][0].content["input"] == "input1"
    assert results[0][1].content["input"] == "input2"
    assert results[0][2].content["input"] == "input3"


def test_expected_result_column_reading(tmp_path):
    csv_content = """input,expected_result
input1,expected1
input2,expected2
input3,expected3"""
    csv_file = tmp_path / "expected_result.csv"
    csv_file.write_text(csv_content)

    config = CSVReaderConfig(
        expected_result_column="expected_result"
    )  # Set the expected_result_column
    reader = CSVReader(config)
    results = list(reader.read(csv_file))

    assert len(results) == 1
    assert len(results[0]) == 3
    assert isinstance(results[0][0], InputData)

    # Check content
    assert results[0][0].content["input"] == "input1"
    assert results[0][1].content["input"] == "input2"
    assert results[0][2].content["input"] == "input3"

    # Check expected results
    assert results[0][0].expected_result == "expected1"
    assert results[0][1].expected_result == "expected2"
    assert results[0][2].expected_result == "expected3"


def test_csv_chunk_size(tmp_path):
    csv_content = """input
""" + "\n".join([f"input{i}" for i in range(1, 105)])  # 104 inputs
    csv_file = tmp_path / "chunk.csv"
    csv_file.write_text(csv_content)

    config = CSVReaderConfig(
        chunk_size=25
    )  # Configuration with a specific chunk size
    reader = CSVReader(config)
    results = list(reader.read(csv_file))

    assert len(results) == 5  # 4 chunks of 25 + 1 chunk of 4
    assert all(len(chunk) == 25 for chunk in results[:-1])
    assert len(results[-1]) == 4


def test_missing_data(tmp_path, caplog):
    csv_content = """input,output
input1,output1
input2,
input3,output3
"""  # Second row is missing data
    csv_file = tmp_path / "missing.csv"
    csv_file.write_text(csv_content)

    config = CSVReaderConfig()  # Default configuration
    reader = CSVReader(config)
    with caplog.at_level(logging.WARNING):
        results = list(reader.read(csv_file))

    # Check if the expected warning message is in the captured logs
    assert any(
        "Missing data on line" in message
        for _, _, message in caplog.record_tuples
    )
    assert len(results) == 1
    assert len(results[0]) == 2  # Excludes the problematic row

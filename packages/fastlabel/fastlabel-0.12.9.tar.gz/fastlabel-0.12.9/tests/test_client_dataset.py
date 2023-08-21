import re
import sys
from pathlib import Path
from uuid import uuid4

import pytest

from fastlabel import Client, FastLabelInvalidException

OBJECT_SIGNED_URL_KEY = "objectSignedUrl"


def remove_object_signed_url(d: dict) -> dict:
    return {k: v for k, v in d.items() if k != OBJECT_SIGNED_URL_KEY}


@pytest.fixture
def client() -> Client:
    return Client()


@pytest.fixture
def testing_image_dataset(client: Client) -> dict:
    # Arrange
    name = f"test-{uuid4()}"
    dataset = client.create_dataset(name=name, slug=name, type="image")
    yield dataset
    # Cleanup
    client.delete_dataset(dataset_id=dataset["id"])


@pytest.fixture
def testing_video_dataset(client: Client) -> dict:
    # Arrange
    name = f"test-{uuid4()}"
    dataset = client.create_dataset(name=name, slug=name, type="video")
    yield dataset
    # Cleanup
    client.delete_dataset(dataset_id=dataset["id"])


@pytest.fixture
def testing_audio_dataset(client: Client) -> dict:
    # Arrange
    name = f"test-{uuid4()}"
    dataset = client.create_dataset(name=name, slug=name, type="audio")
    yield dataset
    # Cleanup
    client.delete_dataset(dataset_id=dataset["id"])


class TestImageDataset:
    def test_find_dataset(self, client: Client, testing_image_dataset: dict):
        # Act
        dataset = client.find_dataset(dataset_id=testing_image_dataset["id"])
        # Assert
        assert dataset == testing_image_dataset

    def test_get_dataset(self, client: Client, testing_image_dataset: dict):
        # Act
        datasets = client.get_datasets(keyword=testing_image_dataset["slug"])
        # Assert
        assert datasets is not None
        assert len(datasets) == 1
        assert datasets[0] == testing_image_dataset

    def test_update_dataset(self, client: Client, testing_image_dataset: dict):
        # Act
        dataset = client.update_dataset(
            dataset_id=testing_image_dataset["id"],
            name="update name",
        )
        # Assert
        assert dataset["name"] == "update name"

    def test_create_dataset_object(self, client: Client, testing_image_dataset: dict):
        # Arrange
        target_file = Path(sys.path[0]) / "files/test_image.jpg"
        # Act
        dataset_object = client.create_image_dataset_object(
            dataset_version_id=testing_image_dataset["version"]["id"],
            name="test_image.jpg",
            file_path=str(target_file),
        )
        # Assert
        assert dataset_object is not None
        assert dataset_object["name"] == "test_image.jpg"
        assert dataset_object["size"] == 6717
        assert dataset_object["height"] == 225
        assert dataset_object["width"] == 225
        assert dataset_object["groupId"] is None

    def test_create_dataset_object_file_type_violation(
        self, client: Client, testing_image_dataset: dict
    ):
        # Arrange
        target_file = Path(sys.path[0]) / "files/test_video.mp4"
        # Act
        with pytest.raises(
            expected_exception=FastLabelInvalidException,
            match=re.escape(
                "<Response [422]> Supported extensions are png, jpg, jpeg."
            ),
        ) as _:
            client.create_image_dataset_object(
                dataset_version_id=testing_image_dataset["version"]["id"],
                name="test_video.mp4",
                file_path=str(target_file),
            )

    def test_find_dataset_object(self, client: Client, testing_image_dataset: dict):
        # Arrange
        target_file = Path(sys.path[0]) / "files/test_image.jpg"
        dataset_object = client.create_image_dataset_object(
            dataset_version_id=testing_image_dataset["version"]["id"],
            name="test_image.jpg",
            file_path=str(target_file),
        )
        # Act
        result = client.find_dataset_object(dataset_object_id=dataset_object["id"])
        # Assert
        assert result["name"] == dataset_object["name"]

    def test_get_dataset_object(self, client: Client, testing_image_dataset: dict):
        # Arrange
        target_file = Path(sys.path[0]) / "files/test_image.jpg"
        dataset_object1 = client.create_image_dataset_object(
            dataset_version_id=testing_image_dataset["version"]["id"],
            name="test_image1.jpg",
            file_path=str(target_file),
        )
        dataset_object2 = client.create_image_dataset_object(
            dataset_version_id=testing_image_dataset["version"]["id"],
            name="test_image2.jpg",
            file_path=str(target_file),
        )
        # Act
        results = client.get_dataset_objects(
            dataset_version_id=testing_image_dataset["version"]["id"]
        )
        # Assert
        assert results is not None
        assert len(results) == 2
        assert remove_object_signed_url(results[0]) == remove_object_signed_url(
            dataset_object1
        )
        assert remove_object_signed_url(results[1]) == remove_object_signed_url(
            dataset_object2
        )

    def test_delete_dataset_object(self, client: Client, testing_image_dataset: dict):
        # Arrange
        target_file = Path(sys.path[0]) / "files/test_image.jpg"
        dataset_object_names = ["test_image1.jpg", "test_image2.jpg", "test_image3.jpg"]
        created = [
            client.create_image_dataset_object(
                dataset_version_id=testing_image_dataset["version"]["id"],
                name=name,
                file_path=str(target_file),
            )
            for name in dataset_object_names
        ]
        dataset_objects = client.get_dataset_objects(
            dataset_version_id=testing_image_dataset["version"]["id"]
        )
        assert dataset_objects is not None
        assert len(dataset_objects) == 3
        for i, dataset_object in enumerate(dataset_objects):
            assert OBJECT_SIGNED_URL_KEY in dataset_object
            assert OBJECT_SIGNED_URL_KEY in created[i]
            assert remove_object_signed_url(dataset_object) == remove_object_signed_url(
                created[i]
            )

        # Act
        client.delete_dataset_objects(
            dataset_id=testing_image_dataset["id"],
            dataset_object_ids=[created[0]["id"], created[2]["id"]],
        )
        # Assert
        results = client.get_dataset_objects(
            dataset_version_id=testing_image_dataset["version"]["id"]
        )
        assert results is not None
        assert len(results) == 1
        assert remove_object_signed_url(results[0]) == remove_object_signed_url(
            created[1]
        )


class TestVideoDataset:
    def test_find_dataset(self, client: Client, testing_video_dataset: dict):
        # Act
        dataset = client.find_dataset(dataset_id=testing_video_dataset["id"])
        # Assert
        assert dataset == testing_video_dataset

    def test_get_dataset(self, client: Client, testing_video_dataset: dict):
        # Act
        datasets = client.get_datasets(keyword=testing_video_dataset["slug"])
        # Assert
        assert datasets is not None
        assert len(datasets) == 1
        assert datasets[0] == testing_video_dataset

    def test_update_dataset(self, client: Client, testing_video_dataset: dict):
        # Act
        dataset = client.update_dataset(
            dataset_id=testing_video_dataset["id"], name="update name"
        )
        # Assert
        assert dataset["name"] == "update name"

    def test_create_dataset_object(self, client: Client, testing_video_dataset: dict):
        # Arrange
        target_file = Path(sys.path[0]) / "files/test_video.mp4"
        # Act
        dataset_object = client.create_video_dataset_object(
            dataset_version_id=testing_video_dataset["version"]["id"],
            name="test_video.mp4",
            file_path=str(target_file),
        )
        # Assert
        assert dataset_object is not None
        assert dataset_object["name"] == "test_video.mp4"
        assert dataset_object["size"] == 534032
        assert dataset_object["height"] == 240
        assert dataset_object["width"] == 320
        assert dataset_object["groupId"] is None

    def test_create_dataset_object_file_type_violation(
        self, client: Client, testing_video_dataset: dict
    ):
        # Arrange
        target_file = Path(sys.path[0]) / "files/test_image.jpg"
        # Act
        with pytest.raises(
            expected_exception=FastLabelInvalidException,
            match=re.escape("<Response [422]> Supported extensions are mp4."),
        ) as _:
            client.create_video_dataset_object(
                dataset_version_id=testing_video_dataset["version"]["id"],
                name="test_image.jpg",
                file_path=str(target_file),
            )

    def test_find_dataset_object(self, client: Client, testing_video_dataset: dict):
        # Arrange
        target_file = Path(sys.path[0]) / "files/test_video.mp4"
        dataset_object = client.create_video_dataset_object(
            dataset_version_id=testing_video_dataset["version"]["id"],
            name="test_video.mp4",
            file_path=str(target_file),
        )
        # Act
        result = client.find_dataset_object(dataset_object_id=dataset_object["id"])
        # Assert
        assert result["name"] == dataset_object["name"]

    def test_get_dataset_object(self, client: Client, testing_video_dataset: dict):
        # Arrange
        target_file = Path(sys.path[0]) / "files/test_video.mp4"
        dataset_object1 = client.create_video_dataset_object(
            dataset_version_id=testing_video_dataset["version"]["id"],
            name="test_video1.mp4",
            file_path=str(target_file),
        )
        dataset_object2 = client.create_video_dataset_object(
            dataset_version_id=testing_video_dataset["version"]["id"],
            name="test_video2.mp4",
            file_path=str(target_file),
        )
        # Act
        results = client.get_dataset_objects(
            dataset_version_id=testing_video_dataset["version"]["id"]
        )
        # Assert
        assert results is not None
        assert len(results) == 2
        assert remove_object_signed_url(results[0]) == remove_object_signed_url(
            dataset_object1
        )
        assert remove_object_signed_url(results[1]) == remove_object_signed_url(
            dataset_object2
        )

    def test_delete_dataset_object(self, client: Client, testing_video_dataset: dict):
        # Arrange
        target_file = Path(sys.path[0]) / "files/test_video.mp4"
        dataset_object_names = ["test_video1.mp4", "test_video2.mp4", "test_video3.mp4"]
        created = [
            client.create_video_dataset_object(
                dataset_version_id=testing_video_dataset["version"]["id"],
                name=name,
                file_path=str(target_file),
            )
            for name in dataset_object_names
        ]

        dataset_objects = client.get_dataset_objects(
            dataset_version_id=testing_video_dataset["version"]["id"]
        )
        assert dataset_objects is not None
        assert len(dataset_objects) == 3
        for i, dataset_object in enumerate(dataset_objects):
            assert OBJECT_SIGNED_URL_KEY in dataset_object
            assert OBJECT_SIGNED_URL_KEY in created[i]
            assert remove_object_signed_url(dataset_object) == remove_object_signed_url(
                created[i]
            )

        # Act
        client.delete_dataset_objects(
            dataset_id=testing_video_dataset["id"],
            dataset_object_ids=[created[0]["id"], created[2]["id"]],
        )
        # Assert
        results = client.get_dataset_objects(
            dataset_version_id=testing_video_dataset["version"]["id"]
        )
        assert results is not None
        assert len(results) == 1
        assert remove_object_signed_url(results[0]) == remove_object_signed_url(
            created[1]
        )


class TestAudioDataset:
    def test_find_dataset(self, client: Client, testing_audio_dataset: dict):
        # Act
        dataset = client.find_dataset(dataset_id=testing_audio_dataset["id"])
        # Assert
        assert dataset == testing_audio_dataset

    def test_get_dataset(self, client: Client, testing_audio_dataset: dict):
        # Act
        datasets = client.get_datasets(keyword=testing_audio_dataset["slug"])
        # Assert
        assert datasets is not None
        assert len(datasets) == 1
        assert datasets[0] == testing_audio_dataset

    def test_update_dataset(self, client: Client, testing_audio_dataset: dict):
        # Act
        dataset = client.update_dataset(
            dataset_id=testing_audio_dataset["id"],
            name="update name",
        )
        # Assert
        assert dataset["name"] == "update name"

    def test_create_dataset_object(self, client: Client, testing_audio_dataset: dict):
        # Arrange
        target_file = Path(sys.path[0]) / "files/test_audio.mp3"
        # Act
        dataset_object = client.create_audio_dataset_object(
            dataset_version_id=testing_audio_dataset["version"]["id"],
            name="test_audio.mp3",
            file_path=str(target_file),
        )
        # Assert
        assert dataset_object is not None
        assert dataset_object["name"] == "test_audio.mp3"
        assert dataset_object["size"] == 16182
        assert dataset_object["height"] == 0
        assert dataset_object["width"] == 0
        assert dataset_object["groupId"] is None

    def test_create_dataset_object_file_type_violation(
        self, client: Client, testing_audio_dataset: dict
    ):
        # Arrange
        target_file = Path(sys.path[0]) / "files/test_image.jpg"
        # Act
        with pytest.raises(
            expected_exception=FastLabelInvalidException,
            match=re.escape(
                "<Response [422]> Supported extensions are mp3, wav and w4a."
            ),
        ) as _:
            client.create_audio_dataset_object(
                dataset_version_id=testing_audio_dataset["version"]["id"],
                name="test_image.jpg",
                file_path=str(target_file),
            )

    def test_find_dataset_object(self, client: Client, testing_audio_dataset: dict):
        # Arrange
        target_file = Path(sys.path[0]) / "files/test_audio.mp3"
        dataset_object = client.create_audio_dataset_object(
            dataset_version_id=testing_audio_dataset["version"]["id"],
            name="test_audio.mp3",
            file_path=str(target_file),
        )
        # Act
        result = client.find_dataset_object(dataset_object_id=dataset_object["id"])
        # Assert
        assert result["name"] == dataset_object["name"]

    def test_get_dataset_object(self, client: Client, testing_audio_dataset: dict):
        # Arrange
        target_file = Path(sys.path[0]) / "files/test_audio.mp3"
        dataset_object1 = client.create_audio_dataset_object(
            dataset_version_id=testing_audio_dataset["version"]["id"],
            name="test_audio1.mp3",
            file_path=str(target_file),
        )
        dataset_object2 = client.create_audio_dataset_object(
            dataset_version_id=testing_audio_dataset["version"]["id"],
            name="test_audio2.mp3",
            file_path=str(target_file),
        )
        # Act
        results = client.get_dataset_objects(
            dataset_version_id=testing_audio_dataset["version"]["id"]
        )
        # Assert
        assert results is not None
        assert len(results) == 2
        assert remove_object_signed_url(results[0]) == remove_object_signed_url(
            dataset_object1
        )
        assert remove_object_signed_url(results[1]) == remove_object_signed_url(
            dataset_object2
        )

    def test_delete_dataset_object(self, client: Client, testing_audio_dataset: dict):
        # Arrange
        target_file = Path(sys.path[0]) / "files/test_audio.mp3"
        dataset_object_names = ["test_audio1.mp3", "test_audio2.mp3", "test_audio3.mp3"]
        created = [
            client.create_audio_dataset_object(
                dataset_version_id=testing_audio_dataset["version"]["id"],
                name=name,
                file_path=str(target_file),
            )
            for name in dataset_object_names
        ]
        dataset_objects = client.get_dataset_objects(
            dataset_version_id=testing_audio_dataset["version"]["id"]
        )
        for i, dataset_object in enumerate(dataset_objects):
            assert OBJECT_SIGNED_URL_KEY in dataset_object
            assert OBJECT_SIGNED_URL_KEY in created[i]
            assert remove_object_signed_url(dataset_object) == remove_object_signed_url(
                created[i]
            )

        # Act
        client.delete_dataset_objects(
            dataset_id=testing_audio_dataset["id"],
            dataset_object_ids=[created[0]["id"], created[2]["id"]],
        )
        # Assert
        results = client.get_dataset_objects(
            dataset_version_id=testing_audio_dataset["version"]["id"]
        )
        assert results is not None
        assert len(results) == 1
        assert remove_object_signed_url(results[0]) == remove_object_signed_url(
            created[1]
        )


class TestDatasetObjectImportHistories:
    def test_get(self, client: Client, testing_image_dataset: dict):
        # Arrange
        target_file = Path(sys.path[0]) / "files/test_image.jpg"
        client.create_image_dataset_object(
            dataset_version_id=testing_image_dataset["version"]["id"],
            name="test_image1.jpg",
            file_path=str(target_file),
        )
        client.create_image_dataset_object(
            dataset_version_id=testing_image_dataset["version"]["id"],
            name="test_image2.jpg",
            file_path=str(target_file),
        )
        # Act
        import_histories = client.get_dataset_object_import_histories(
            dataset_version_id=testing_image_dataset["version"]["id"]
        )
        # Assert
        assert import_histories is not None
        assert len(import_histories) == 2
        assert import_histories[0]["type"] == "local"
        assert import_histories[0]["status"] == "completed"
        assert import_histories[0]["msgCode"] == "none"
        assert import_histories[0]["msgLevel"] == "none"
        assert import_histories[0]["userName"] is not None
        assert import_histories[0]["count"] == 1
        assert import_histories[0]["type"] == "local"
        assert import_histories[0]["status"] == "completed"
        assert import_histories[0]["msgCode"] == "none"
        assert import_histories[0]["msgLevel"] == "none"
        assert import_histories[0]["userName"] is not None
        assert import_histories[0]["count"] == 1

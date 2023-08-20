from .utils import host_target_from_url


def test_host_target_from_url():
    url = "https://test_domain/test_path"

    host, target = host_target_from_url(url)

    assert host == "test_domain"
    assert target == "/test_path"

from basic_ci.services.id_service import UIDService


def test_generate_run_id_is_unique():
    service = UIDService()
    ids = {service.generate_run_id("abc123") for _ in range(1000)}
    assert len(ids) == 1000


def test_generate_run_id_is_lowercase_and_hex():
    service = UIDService()
    run_id = service.generate_run_id("ABCDEF")

    assert run_id == run_id.lower()
    assert all(c in "0123456789abcdef" for c in run_id)


def test_generate_run_id_length_bounds():
    service = UIDService()

    short_id = service.generate_run_id(length=8)
    long_id = service.generate_run_id(length=100)

    assert len(short_id) < 12
    assert len(long_id) <= 64

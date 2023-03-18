import pytest

def test_user_str(base_user):
    """Test custom user model string representation."""
    assert base_user.__str__() == f"{base_user.username}"
    
def test_user_short_name(base_user):
    """Test that the user model short name method works correctly"""
    short_name = f"{base_user.username}"
    assert base_user.get_short_name() == short_name
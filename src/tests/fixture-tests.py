def test_seller_password_valid_password(seller, valid_password):
    assert seller.password != valid_password, 'Bug in tests: seller.password should not be equal to valid password'

from data.user_data import VALID_USER

SETTING_USER_1 = {
    "url": "https://i.namu.wiki/i/WxfZN24op278LD9Zs0CqcmmDTf5BrsxEj-jKSFSKGshojImAMcxAQET1l6DX5pmCKffUsSm65A1T0yUg0RVILEiobkjl4EHQvprjO7BOl7zzUZv6NjFkt8G1j7O1n98hvxqYx6pUyCLFiSR3hLbwRg.webp",
    "username": "SampleUser1",
    "bio": "Sample bio 1",
    "email": "SampleUser1@example.com",
    "password":"samplepwd1"
}

SETTING_USER_2 = {
    "url": "https://item.kakaocdn.net/do/eca065fa2b45d3cc588798b70ee7ec2ff43ad912ad8dd55b04db6a64cddaf76d",
    "username": "SampleUser2",
    "bio": "Sample bio 2",
    "email": "SampleUser2@example.com",
    "password":"samplepwd2"
}

SETTING_USER_3 = {
    "url": "Wrong_URL",
    "username": "SampleUser3",
    "bio": "Sample bio 3",
    "email": "SampleUser3@example.com",
    "password":"samplepwd3"
}

ARTICLE_DATA_1 = (f"{VALID_USER['username']}_작성 테스트", "테스트 주제", "테스트 게시글 본문입니다.", ["태그1", "태그2"])

ARTICLE_DATA_2 = (f"{VALID_USER['username']}_수정 테스트", "테스트 수정", "테스트 게시글 수정한 본문입니다.", ["추가 태그1", "추가 태그2"])

COMMENT_DATA_1 = "댓글"

SIGN_UP_ERROR_TEXT_DATA = [ 
    ("", "", "", "email can't be blank", "사용자명, 이메일, 비밀번호 입력창을 모두 공백"),
    (VALID_USER["username"], "", "", "email can't be blank", "이메일, 비밀번호 입력창을 공백"),
    (VALID_USER["username"], VALID_USER["email"], "", "password can't be blank", "비밀번호 입력창을 공백"),
    (VALID_USER["username"], VALID_USER["email"], VALID_USER["password"], ["email has already been taken", "username has already been taken"], "가입된 사용자명, 이메일")
]

SIGN_IN_ERROR_TEXT_DATA = [ 
    ("", "", "email can't be blank", "이메일 및 비밀번호 입력창 모두 공백"),
    ("", VALID_USER["password"], "email can't be blank", "이메일 입력창을 공백"),
    (VALID_USER["email"], "", "password can't be blank", "비밀번호 입력창을 공백"),
    (VALID_USER["email"], "wrong_password", "email or password is invalid", "맞지 않는 비밀번호"),
    ("wrong@email.com", VALID_USER["password"], "email or password is invalid", "미가입 이메일")
]

EMAIL_VALIDATION_TEXT_DATA = [
    ("user", "이메일 주소에 '@'를 포함해 주세요. 'user'에 '@'가 없습니다."),
    ("@", "'@' 앞 부분을 입력해 주세요. '@'(이)가 완전하지 않습니다."),
    ("user@", "'@' 뒷 부분을 입력해 주세요. 'user@'(이)가 완전하지 않습니다.")
]
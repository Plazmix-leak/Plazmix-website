from pydantic import BaseModel


class UserImageVariantSizesDataClass(BaseModel):
    size_100: str
    size_150: str
    size_300: str


class UserImageVariantsDataClass(BaseModel):
    avatar: UserImageVariantSizesDataClass
    head: UserImageVariantSizesDataClass
    bust: UserImageVariantSizesDataClass
    body: UserImageVariantSizesDataClass


class UserImageDataClass(BaseModel):
    identifier: str
    skin_raw: str
    variants: UserImageVariantsDataClass


class UserImage:
    def __init__(self, identification):
        self._identification = identification

    @property
    def data_class(self) -> UserImageDataClass:
        avatar = UserImageVariantSizesDataClass(size_100=self.avatar(100), size_150=self.avatar(150),
                                                size_300=self.avatar(300))

        head = UserImageVariantSizesDataClass(size_100=self.head(100), size_150=self.head(150),
                                              size_300=self.head(300))

        bust = UserImageVariantSizesDataClass(size_100=self.bust(100), size_150=self.bust(150),
                                              size_300=self.bust(300))

        body = UserImageVariantSizesDataClass(size_100=self.body(100), size_150=self.body(150),
                                              size_300=self.body(300))

        variants = UserImageVariantsDataClass(avatar=avatar,
                                              head=head,
                                              bust=bust,
                                              body=body)

        return UserImageDataClass(variants=variants, skin_raw=self.skin(),
                                  identifier=self._identification)

    def avatar(self, size: int = None):
        return f"https://minotar.net/avatar/{self._identification}/{size}.png"

    def head(self, size: int = None):
        return f"https://minotar.net/cube/{self._identification}/{size}.png"

    def body(self, size: int = None):
        return f"https://minotar.net/armor/body/{self._identification}/{size}.png"

    def bust(self, size: int = None):
        return f"https://minotar.net/armor/bust/{self._identification}/{size}.png"

    def skin(self):
        return f"https://minotar.net/skin/{self._identification}"

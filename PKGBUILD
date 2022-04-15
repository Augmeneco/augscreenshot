# Maintainer: Cha14ka <cha14ka@yandex.ru>
pkgname=augscreenshot
pkgver=1.0
pkgrel=1
pkgdesc="AugScreenshot - program for do screenshots on phosh with popup notifications"
arch=('any')
url="https://github.com/Augmeneco/augscreenshot"
license=('GPL3')
depends=('notify-send.sh' 'python-pyqt6' 'dos2unix')
source=("git+https://github.com/Augmeneco/augscreenshot")
md5sums=('SKIP')

prepare() {
    cd "$pkgname"

    dos2unix *.py
}

package() {
    cd "$pkgname"

    mkdir -p $pkgdir$HOME/.local/share/augscreen
    mkdir -p $pkgdir$HOME/.local/share/applications
    mkdir -p $pkgdir/usr/share/pixmaps/

    chmod -R 700 $pkgdir/home/*

    cp icon.png $pkgdir/usr/share/pixmaps/augscreen.png
    cp *.py $pkgdir$HOME/.local/share/augscreen/
    cp augscreen.desktop $pkgdir$HOME/.local/share/applications/

    install -Dm0755 augscreen "$pkgdir/usr/bin/augscreen"
}

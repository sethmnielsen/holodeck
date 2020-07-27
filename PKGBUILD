# Maintainer: Seth Nielsen <sethnielsen64@gmail.com>
pkgname=('python-holodeck')
_pkgname=holodeck
pkgver=0.3.1
pkgrel=1
pkgdesc="High fidelity simulated environments for reinforcement learning"
arch=('any')
url="https://github.com/byu-pccl/holodeck"
license=('MIT')
depends=('python-posix_ipc' 'python-numpy')
makedepends=('python-setuptools')
optdepends=('opencv')

package() {
    cd $srcdir/..
    python setup.py install --root="$pkgdir" --optimize=1
}

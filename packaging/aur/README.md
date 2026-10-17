# Publishing FloatBoard to AUR (Arch User Repository)

Package name: **`floatboard-bin`**

### Steps to publish:

1. **Create an account on AUR:**
   Go to [aur.archlinux.org/register](https://aur.archlinux.org/register/) and create an account.

2. **Add your SSH key to AUR:**
   Copy your public key:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   # or
   cat ~/.ssh/id_rsa.pub
   ```
   Paste it into: **AUR -> My Account -> SSH Public Key**.

3. **Clone the empty package repository from AUR:**
   ```bash
   git clone ssh://aur@aur.archlinux.org/floatboard-bin.git
   ```

4. **Copy `PKGBUILD` and `.SRCINFO` into the cloned folder:**
   ```bash
   cp PKGBUILD .SRCINFO floatboard-bin/
   cd floatboard-bin
   ```

5. **Commit and push to AUR:**
   ```bash
   git add PKGBUILD .SRCINFO
   git commit -m "Initial release v1.0.20"
   git push origin master
   ```

Once pushed, all Arch Linux, Manjaro, and EndeavourOS users can immediately install FloatBoard with:
```bash
yay -S floatboard-bin
# or
paru -S floatboard-bin
```

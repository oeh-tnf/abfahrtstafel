let
  admins = builtins.concatMap (admin: admin.sshKeys) (builtins.attrValues (import ../../admins));
  tnf-abfahrtstafel = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIECVboWI8EOWy+vPIuQZryudZTNbWHD/gRK5aJjOvb+d root@tnf-abfahrtstafel";
in
{
  "wifi.age".publicKeys = admins ++ [ tnf-abfahrtstafel ];
}

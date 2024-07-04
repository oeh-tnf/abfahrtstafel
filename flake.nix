{
  inputs = {
    nixpkgs.url = github:NixOS/nixpkgs/nixos-23.11;
    systems.url = github:nix-systems/default;
  };

  outputs = { self, nixpkgs, systems }: {
    packages =
      let
        eachSystem = nixpkgs.lib.genAttrs (import systems);
      in
      eachSystem (system: {
        default = nixpkgs.legacyPackages.${system}.callPackage app/package.nix {
          waveshare-epd = self.packages.${system}.waveshare-epd;
        };
        waveshare-epd = nixpkgs.legacyPackages.${system}.callPackage nix-support/waveshare-epd.nix {};
      });
  };
}


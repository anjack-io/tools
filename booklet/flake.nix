{
  description = "PDF booklet tools";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.05";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };
        tex = pkgs.texlive.combine {
          inherit (pkgs.texlive) scheme-small pdfjam;
        };
      in {
        devShells.default = pkgs.mkShell {
          packages = [
            tex
            pkgs.qpdf
            pkgs.poppler_utils
          ];
        };
      });
}

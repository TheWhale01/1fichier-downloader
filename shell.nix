{ pkgs ? import <nixpkgs> {}, ... }:

pkgs.mkShell {
	nativeBuildInputs = with pkgs; [
		python3
		python3.pkgs.pip
		geckodriver
		firefox
	];
}

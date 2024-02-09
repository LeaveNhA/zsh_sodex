<h1 align="center">⌨️ 🦾 Zsh SOdex forked from Zsh Codex</h1>

<p align="center">
    AI in the command line with Guidance!
</p>

<p align="center">
    <a href="https://github.com/LeaveNhA/zsh_codex/stargazers"
        ><img
            src="https://img.shields.io/github/stars/LeaveNhA/zsh_codex?colorA=2c2837&colorB=c9cbff&style=for-the-badge&logo=starship style=flat-square"
            alt="Repository's starts"
    /></a>
    <a href="https://github.com/LeaveNhA/zsh_codex/issues"
        ><img
            src="https://img.shields.io/github/issues-raw/LeaveNhA/zsh_codex?colorA=2c2837&colorB=f2cdcd&style=for-the-badge&logo=starship style=flat-square"
            alt="Issues"
    /></a>
    <a href="https://github.com/LeaveNhA/zsh_codex/blob/main/LICENSE"
        ><img
            src="https://img.shields.io/github/license/LeaveNhA/zsh_codex?colorA=2c2837&colorB=b5e8e0&style=for-the-badge&logo=starship style=flat-square"
            alt="License"
    /><br />
    <a href="https://github.com/LeaveNhA/zsh_codex/commits/main"
		><img
			src="https://img.shields.io/github/last-commit/LeaveNhA/zsh_codex/main?colorA=2c2837&colorB=ddb6f2&style=for-the-badge&logo=starship style=flat-square"
			alt="Latest commit"
    /></a>
    <a href="https://github.com/LeaveNhA/zsh_codex"
        ><img
            src="https://img.shields.io/github/repo-size/LeaveNhA/zsh_codex?colorA=2c2837&colorB=89DCEB&style=for-the-badge&logo=starship style=flat-square"
            alt="GitHub repository size"
    /></a>
</p>

<p align="center">
    <img src='https://github.com/LeaveNhA/bins/raw/main/zsh_codex/zc4.gif'>
    <p align="center">
        You just need to write a comment or variable name and the AI will write the corresponding code.
    </p>
</p>


## What is it?

This is a ZSH plugin that enables you to use OpenAI's powerful SOdex AI in the command line. OpenAI SOdex is the AI that also powers GitHub Copilot.
To use this plugin you need to get access to OpenAI's [Codex API](https://openai.com/blog/openai-codex/).


## How do I install it?
### Manual Installation
1. Install the OpenAI package.
```
pip3 install openai guidance
```

2. Download the ZSH plugin.

```
git clone https://github.com/LeaveNhA/zsh_sodex.git ~/.oh-my-zsh/custom/plugins/zsh_sodex
```

3. Add the following to your `.zshrc` file.

Using oh-my-zsh:
```
    plugins=(zsh_codex)
    bindkey '^X' create_completion
```
Without oh-my-zsh:
```
    # in your/custom/path you need to have a "plugins" folder and in there you clone the repository as zsh_codex
    export ZSH_CUSTOM="your/custom/path"
    source "$ZSH_CUSTOM/plugins/zsh_sodex/zsh_sodex.plugin.zsh"
    bindkey '^X' create_completion
```

5. Run `zsh`, start typing and complete it using `^X`!

[Traffic Statistics](https://LeaveNhA.github.io/github_repo_stats_data/LeaveNhA/zsh_codex/latest-report/report.html)

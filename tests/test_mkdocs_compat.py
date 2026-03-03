from hooks.mkdocs_compat import on_startup


def test_mistune_compat_alias_is_installed():
    from mistune.block_parser import BlockParser

    on_startup(command="build", dirty=False)

    assert hasattr(BlockParser, "parse_axt_heading")
    assert BlockParser.parse_axt_heading is BlockParser.parse_atx_heading

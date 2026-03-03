"""MkDocs compatibility hooks for local build-time dependency mismatches."""

def on_startup(**kwargs):
    """Patch Mistune for older nbconvert releases bundled in existing envs."""
    try:
        from mistune.block_parser import BlockParser

        if not hasattr(BlockParser, "parse_axt_heading") and hasattr(BlockParser, "parse_atx_heading"):
            BlockParser.parse_axt_heading = BlockParser.parse_atx_heading
    except Exception:
        # If the dependency graph changes, leave the build untouched.
        pass

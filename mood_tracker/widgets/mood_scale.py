from textual.widgets import Static


class MoodScale(Static):
    """Displays a simple mood scale legend."""

    def on_mount(self) -> None:
        self.update(
            "Mood scale:\n"
            "[red]1-3[/red] 😫  [yellow]4-6[/yellow] 😐  [green]7-10[/green] 😄"
        )
        self.styles.margin_top = 1
        self.styles.margin_bottom = 1
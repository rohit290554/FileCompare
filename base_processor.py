class FileProcessor:
    """Base class for file processors."""

    @staticmethod
    def highlight_differences(text1, text2):
        """Highlight differences between two texts word by word."""
        words1 = text1.split()
        words2 = text2.split()

        highlighted = []
        for w1, w2 in zip(words1, words2):
            if w1 != w2:
                highlighted.append(f"{{{w1}/{w2}}}")
            else:
                highlighted.append(w1)

        highlighted.extend(words1[len(words2):] if len(words1) > len(words2) else words2[len(words1):])
        return ' '.join(highlighted)

# Contributing to Football Analysis & Player Tracking System

First off, thank you for considering contributing to this project! 🎉

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- **Description**: Clear and concise description of the bug
- **Steps to reproduce**: Detailed steps to reproduce the behavior
- **Expected behavior**: What you expected to happen
- **Actual behavior**: What actually happened
- **Environment**: 
  - OS (Windows/Linux/Mac)
  - Python version
  - Package versions (`pip list`)
- **Screenshots/Videos**: If applicable
- **Additional context**: Any other relevant information

### Suggesting Enhancements

Enhancement suggestions are welcome! Please include:

- **Use case**: Why this enhancement would be useful
- **Proposed solution**: How you envision it working
- **Alternatives considered**: Other approaches you've thought about
- **Additional context**: Screenshots, mockups, examples

### Pull Requests

1. **Fork the repository** and create your branch from `main`:
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. **Make your changes**:
   - Write clear, commented code
   - Follow the existing code style
   - Add tests if applicable
   - Update documentation as needed

3. **Test your changes**:
   ```bash
   python main.py  # Ensure it runs without errors
   ```

4. **Commit your changes**:
   ```bash
   git commit -m "Add amazing feature"
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/amazing-feature
   ```

6. **Open a Pull Request** with:
   - Clear title and description
   - Reference any related issues
   - Screenshots/videos if UI changes

## Code Style Guidelines

### Python Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise

Example:
```python
def calculate_distance(point1, point2):
    """
    Calculate Euclidean distance between two points.
    
    Args:
        point1 (tuple): (x, y) coordinates of first point
        point2 (tuple): (x, y) coordinates of second point
        
    Returns:
        float: Distance between the points
    """
    return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)**0.5
```

### Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and pull requests when relevant

Good examples:
```
Add player speed calculation feature
Fix ball interpolation for missing detections
Update README with installation instructions
```

## Development Setup

1. **Clone and setup**:
```bash
git clone https://github.com/AhmedHassan1722/Football_Analysis.git
cd Football_Analysis
python -m venv FB
source FB/bin/activate  # On Windows: FB\Scripts\activate
pip install -r requirements.txt
```

2. **Make your changes**

3. **Test thoroughly** with different videos and scenarios

## Areas for Contribution

Here are some areas where contributions would be particularly valuable:

- **Performance optimization**: Faster processing, reduced memory usage
- **Model improvements**: Better detection accuracy, new model integrations
- **Features**: New analytics, statistics, or visualization options
- **Documentation**: Tutorials, examples, API documentation
- **Testing**: Unit tests, integration tests
- **Bug fixes**: Address issues in the issue tracker

## Questions?

Feel free to open an issue with your question or reach out to the maintainers.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🙏⚽

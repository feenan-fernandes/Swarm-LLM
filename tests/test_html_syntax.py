import re

def test_html():
    with open('templates/index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    m = re.search(r'<script type="text/babel">(.*?)</script>', content, re.DOTALL)
    assert m is not None, 'No babel script found!'
    script = m.group(1)
    script = script.replace('{% raw %}', '').replace('{% endraw %}', '')

    stack = []
    pairs = {'}': '{', ')': '(', ']': '['}
    for i, ch in enumerate(script):
        if ch in '{[(':
            stack.append((ch, i))
        elif ch in '}])':
            if not stack:
                raise ValueError(f'Extra closing {ch} at char {i}')
            top, pos = stack.pop()
            if top != pairs[ch]:
                raise ValueError(f'Mismatched {top} at {pos} closed by {ch} at {i}')

    if stack:
        top, pos = stack[-1]
        raise ValueError(f'Unclosed {top} from char {pos}')
    print(f'JSX & JS bracket balancing test PASSED! Script size: {len(script)} chars.')

if __name__ == '__main__':
    test_html()

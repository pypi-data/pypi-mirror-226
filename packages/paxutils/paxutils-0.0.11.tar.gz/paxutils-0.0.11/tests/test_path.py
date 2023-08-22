from paxutils.path import Path

path = Path('narcity.csv', course='GIF-U016')
print(path, path.exists(), path._path_index)

path /= 'toto'
print(path, type(path), path._path_index)

print('tata' / path)

path = Path('/narcity.csv', course='GIF-U016')
print(path, path.exists(), path._path_index)

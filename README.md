# eml2md

[![codecov](https://codecov.io/gh/elda27/eml2md/branch/main/graph/badge.svg?token=Ck30XyeFvG)](https://codecov.io/gh/elda27/eml2md)

`eml2md` is a command line tool for converting from eml to markdown.

## Example

```bash
eml2md -i tests/example/Test.eml -o Test.md
```

```markdown
|         |                                                                          |
| ------- | ------------------------------------------------------------------------ |
| From    | 井炉波鳰惠土 <author2@example.com>                                       |
| To      | 井炉波鳰惠土 <author1@example.com><br>井炉波鳰惠土 <author2@example.com> |
| CC      | 井炉波鳰惠土 <author2@example.com><br> <author1@example.com>             |
| Date    | 2022-08-09 23:47:29                                                      |
| Subject | Re: Test                                                                 |

test blanks
2022 年 8 月 9 日(火) 23:47 井炉波鳰惠土 <author1@example.com>:

> Quote message
>
> dsadbubfdus[\
> dsadinadioa
>
> dsnaidnai
>
> dsnuandi
```

## Usage

```bash
usage: eml2md [-h] -i INPUT -o OUTPUT [-f {simple,html}]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input file
  -o OUTPUT, --output OUTPUT
                        Output file
  -f {simple,html}, --format {simple,html}
                        Format of output markdown
```

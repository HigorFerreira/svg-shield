from socket import (
    socket,
    AF_INET,
    SOCK_STREAM
)

import urllib.parse as parse

def getImage(name: str = 'Text', version: str = "@vers", pcolor: str = "#00383e", scolor: str = "#fdffff") -> bytes:
    return f"""
<svg
    width="130"
    height="29.103001"
    viewBox="0 0 34.395833 7.7001688"
    version="1.1"
    xmlns="http://www.w3.org/2000/svg">
    <defs>
        <style>
            .fill-default{{
                fill:{pcolor};
            }}
            .stroke-default{{
                stroke:{pcolor};
            }}
            .s-fill-default{{
                fill:{scolor};
            }}

            .t {{
                font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-family:sans-serif;-inkscape-font-specification:sans-serif;
            }}

            .stroke-width{{
                stroke-width:0.132292;
            }}

            .paint-order {{
                paint-order:fill markers stroke
            }}

            .size1{{
                font-size:4.23333px;
            }}

            .size2{{
                font-size:3.52778px;
            }}

            .text-center{{
                text-align:center;
            }}

            .text-amiddle{{
                text-anchor:middle;
            }}

            .rect1{{
                stroke-width:0.141518;
            }}
            .rect2{{
                fill:none;stroke-width:0.150019;
            }}
        </style>
    </defs>
    <g>
        <text
            xml:space="preserve"
            class="text-center text-amiddle size1 stroke-width paint-order fill-default"
            x="15.98409"
            y="5.3631639"
        >
            <tspan
                class="t stroke-width size1"
                x="15.98409"
                y="5.3631639">{name}</tspan>
        </text>
        <rect
            class="rect1 paint-order fill-default"
            width="16.719423"
            height="7.7318883"
            x="17.608616"
            y="-0.015864464"
            ry="0.59066111" />
        <text
            xml:space="preserve"
            class="t stroke-width size2 paint-order s-fill-default"
            x="18.759525"
            y="4.8526049"><tspan
                class="stroke-width size2 s-fill-default"
                x="18.759525"
                y="4.8526049">{version}</tspan></text>
        <rect
            class="rect2 paint-order stroke-default"
            width="34.245815"
            height="7.5500774"
            x="0.075008869"
            y="0.075047404"
            ry="0.57295603"/>
    </g>
</svg>
""".encode("utf8")

def main():
    server = socket(AF_INET, SOCK_STREAM)
    server.bind(('0.0.0.0', 8080))
    server.listen()

    while True:
        client, addr = server.accept()

        req = client.recv(1024).split(b'\r\n')
        try:
            path = req[0].split(b' ')[1].decode('utf8')
            args = parse.unquote_plus(path).split('/')
            args.pop(0)
        except Exception:
            args = ['']

        print(args)

        if args[0] and len(args) > 0 and len(args) < 5:
            image = getImage(*args)
        else:
            image = getImage()

        client.sendall(
            b"".join([
                (
                    f"HTTP/1.1 200 OK\r\n"
                    f"Content-Type: image/svg+xml\r\n"
                    f"Content-Length: {len(image)}\r\n"
                    f"\r\n"
                ).encode("utf-8"),
                image,
                b"\r\n"
            ])
        )

if __name__ == "__main__":
    main()
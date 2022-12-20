import base64
from io import BytesIO


def generate_fig_data(fig):
    buf = BytesIO()
    fig.savefig(buf, format='png')
    data = base64.b64encode(buf.getbuffer()).decode('ASCII')
    return f'data:image/png;base64,{data}'

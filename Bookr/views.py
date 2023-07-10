import io
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import plotly.graph_objs as graph
from plotly.offline import plot
from .utils import get_books_read_by_month, get_books_read
import xlsxwriter
from io import BytesIO




@login_required
def profile(request):
    user = request.user
    permissions = user.get_all_permissions()
    # Get the books read in different months this year
    books = get_books_read_by_month(user.username)

    """
    Initialize the Axis for graphs, X-Axis is months,
    Y-axis is books read
    """
    months = [1+i for i in range(12)]
    books_read = [0 for _ in range(12)]

    # Set the value for books read per month on Y-Axis
    for book in books:
        list_index = book['date_created__month'] - 1
        books_read[list_index] = book['book_count']

    # Generate a scatter plot HTML
    figure = graph.Figure()
    scatter = graph.Scatter(x=months, y=books_read)
    figure.add_trace(scatter)
    figure.update_layout(xaxis_title='Month', yaxis_title="No. of books read")
    plot_html = plot(figure, output_type='div')

    context = {
        'user': user,
        'permissions': permissions,
        'books_read_plot': plot_html
    }

    return render(request, "profile.html", context)


@login_required
def reading_history(request):
    user = request.user
    # Get books
    books_read = get_books_read(user.username)
    books_read = books_read
    # Create xlsx on memory instead of disk
    temp_file = io.BytesIO()

    # Create xlsx work book
    workbook = xlsxwriter.Workbook(temp_file)

    # Add sheet for work book
    sheet = workbook.add_worksheet()

    # Write data to sheet
    for row in range(len(books_read)):
        for col in range(2):
            if col == 0:
                book = books_read[row]['book__title']
                sheet.write(row, col, book)
            else:
                book = str(books_read[row]['date_created'])
                sheet.write(row, col, book)
    workbook.close()

    # Retrieved the data stored inside the in-memory binary file
    data_to_download = temp_file.getvalue()

    # Prepared an HTTP response with the ms-excel content type
    response = HttpResponse(content_type='application/vnd.ms-excel')

    # Indicated that this response should be treated as a downloadable file
    response['Content-Disposition'] = 'attachment; filename=reading_history.xlsx'
    response.write(data_to_download)
    temp_file.close()

    return response

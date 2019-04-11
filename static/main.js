function bookSearch() {
    var search = document.getElementById("search").value
    document.getElementById("results").innerHTML = ""
    console.log(search)

    $.ajax({
        url: "https://www.googleapis.com/books/v1/volumes?q=" + search + "&max-results=20",
        dataType: "json",

        success: function (data) {
            console.log(data);
            var html = '';


            var count = 0;
            for (i = 0; i < data.items.length; i++) {


                if (count === 0) html += "<div class='row form-group'>";

                var isbn_10 = '';
                if (data.items[i].volumeInfo.industryIdentifiers.length > 1) {
                    isbn_10 = data.items[i].volumeInfo.industryIdentifiers[1].identifier;
                }
                html += "<div class='col col-md-4 form-group text-center'>";
                html += '<input type = "hidden" id = "title' + i + '" value = "' + data.items[i].volumeInfo.title + '" >'
                html += '<input type="hidden" id="image' + i + '" value="' + data.items[i].volumeInfo.imageLinks.thumbnail + '">'
                html += '<input type="hidden" id="author' + i + '" value="' + data.items[i].volumeInfo.authors + '">'
                html += '<input type="hidden" id="ISBN_13' + i + '" value="' + data.items[i].volumeInfo.industryIdentifiers[0].identifier + '">'
                html += '<input type="hidden" id="ISBN_10' + i + '" value="' + isbn_10 + '">'
                html += '<input type="hidden" id="date_published' + i + '" value="' + data.items[i].volumeInfo.publishedDate + '">'
                html += '<input type="hidden" id="description' + i + '" value="' + data.items[i].volumeInfo.description + '">'
                html += '<input type="hidden" id="total_pages' + i + '" value="' + data.items[i].volumeInfo.pageCount + '">'
                html += "<img width='165px' height='248px' src=' " + data.items[i].volumeInfo.imageLinks.thumbnail + " ' />";
                html += '<a onclick="detailsClick(' + i + ')" type="button" class="details-btn" data-toggle="modal" data-target="#exampleModal"><img src="/static/images/buttons/add1.svg"></a>'


                //     results.innerHTML += "<div>" + data.items[i].volumeInfo.title + "</div>",
                //     results.innerHTML += "<div> By: " + data.items[i].volumeInfo.authors + "</div>"
                // results.innerHTML += "<div> ISBN-13: " + data.items[i].volumeInfo.industryIdentifiers[0].identifier + "</div>"
                // results.innerHTML += "<div> ISBN-10: " + data.items[i].volumeInfo.industryIdentifiers[1].identifier + "</div>"
                // results.innerHTML += "<div> Date published: " + data.items[i].volumeInfo.publishedDate + "</div>"
                // results.innerHTML += "<div> Total pages: " + data.items[i].volumeInfo.pageCount + "</div>"
                // results.innerHTML += "<div> Description: " + data.items[i].volumeInfo.description + "</div>"
                html += "</div>";
                count++;
                if (count === 6) {
                    html += "</div>";
                    count = 0;
                }
            }
            html += "</div>";
            results.innerHTML = html;
        },

        type: "GET"
    });
}

document.getElementById("search-button").addEventListener("click", bookSearch, false)

function detailsClick(index) {
    //alert('copy details to modal ' + index)
    $('#exampleModalLabel').text($('#title' + index).val());
    $('#md_image').attr('src', $('#image' + index).val());
    $('#md_author').text($('#author' + index).val());
    $('#md_ISBN_13').text($('#ISBN_13' + index).val());
    $('#md_ISBN_10').text($('#ISBN_10' + index).val());
    $('#md_date_published').text($('#date_published' + index).val());
    $('#md_description').text($('#description' + index).val());
    $('#md_total_pages').text($('#total_pages' + index).val());
    $('#title').val($('#title' + index).val());
    $('#image').val($('#image' + index).val());
    $('#author').val($('#author' + index).val());
    $('#ISBN_13').val($('#ISBN_13' + index).val());
    $('#ISBN_10').val($('#ISBN_10' + index).val());
    $('#date_published').val($('#date_published' + index).val());
    $('#description').val($('#description' + index).val());
    $('#total_pages').val($('#total_pages' + index).val());
}



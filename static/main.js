function bookSearch() {
    var search = document.getElementById("search").value
    document.getElementById("results").innerHTML = ""
    console.log(search)

    $.ajax({
        url: "https://www.googleapis.com/books/v1/volumes?q=" + search,
        dataType: "json",

        success: function (data) {
            console.log(data);
            var html = '';


            var count = 0;
            for (i = 0; i < data.items.length; i++) {


                if (count === 0) html += "<div class='row'>";

                html += "<div class='col col-md-2'>";
                html += "<form method='POST' action='' novalidate>";
                html += "<input type = 'hidden' name = 'title' value = '" + data.items[i].volumeInfo.title + "' >"
                html += '<input type="hidden" name="image" value="">'
                html += '<input type="hidden" name="author" value="">'
                html += '<input type="hidden" name="ISBN_13" value="">'
                html += '<input type="hidden" name="ISBN_10" value="">'
                html += '<input type="hidden" name="date_published" value="">'
                html += '<input type="hidden" name="description" value="">'
                html += '<input type="hidden" name="total_pages" value="">'
                html += "<img width='165px' height='248px' src=' " + data.items[i].volumeInfo.imageLinks.thumbnail + " ' />";
                html += "<button>Details</button>"
                html += '</form >'
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
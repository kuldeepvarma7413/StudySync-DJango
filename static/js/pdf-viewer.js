$(function () {
    // Get the PDF URL from the data-pdf-url attribute
    const pdfUrl = () => {
        const embed = document.querySelector('.view-pdf-btn');
        const url = embed ? embed.getAttribute('data-pdf-url') : null;
        console.log(url); // Check if the URL is correct
        return url;
    }

    // Initialize PDF viewer
    const initPDFViewer = (pdfUrl) => {
        $("#pdfViewerDiv").html("");

        // create watermark
        let watermark = document.createElement("p");
        let watermark1 = document.createElement("p");
        let watermark2 = document.createElement("p");
        watermark.classList.add("watermark"); 
        watermark1.classList.add("watermark"); 
        watermark2.classList.add("watermark"); 
        watermark.textContent="StudySync StudySync StudySync ";
        watermark1.textContent="StudySync StudySync StudySync ";
        watermark2.textContent="StudySync StudySync StudySync ";
        watermark.style.top="-103px";
        watermark.style.left="0px";
        watermark1.style.top="183px";
        watermark1.style.left="250px";
        watermark2.style.top="306px";
        watermark2.style.left="650px";
       


        pdfjsLib.getDocument(pdfUrl).promise.then(pdfDoc => {
            let pages = pdfDoc.numPages; // Use pdfDoc.numPages instead of pdfDoc._pdfInfo.numPages

            for (let i = 1; i <= pages; i++) {
                pdfDoc.getPage(i).then(page => {
                    let pdfCanvas = document.createElement("canvas");
                    let context = pdfCanvas.getContext("2d");
                    let pageViewPort = page.getViewport({ scale: 1 });

                    pdfCanvas.width = pageViewPort.width; // Adjust as needed
                    pdfCanvas.height = pageViewPort.height;

                    // Adjust the style to display pages vertically
                    pdfCanvas.style.display = "block";
                    pdfCanvas.style.margin = "10px auto";
                    pdfCanvas.style.height = pageViewPort.height + "px"; // Fixed height for each page
                    $("#pdfViewerDiv").append(pdfCanvas);

                    page.render({
                        canvasContext: context,
                        viewport: pageViewPort
                    })
                }).catch(pageErr => {
                    console.log(pageErr);
                })
            }
        }).catch(pdfErr => {
            console.log(pdfErr);
        })
        // add watermark
        $("body").append(watermark);
        $("body").append(watermark1);
        $("body").append(watermark2);
    }

    // Call the PDF viewer initialization
    const url = pdfUrl();
    if (url) {
        initPDFViewer(url);
    }
});

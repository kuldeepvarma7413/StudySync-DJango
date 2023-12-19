$(function () {
    const pdfUrl = () => {
        const embed = document.querySelector('.view-pdf-btn');
        let url = embed ? embed.getAttribute('data-pdf-url') : null;
        url = url.split('/media/')[1] + "/media/" + url.split('/media/')[2];
        return url;
    }

    const initPDFViewer = (pdfUrl) => {
        $(".pdf-container").html("");

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
            let pages = pdfDoc.numPages;

            for (let i = 1; i <= pages; i++) {
                pdfDoc.getPage(i).then(page => {
                    let pdfCanvas = document.createElement("canvas");
                    let context = pdfCanvas.getContext("2d");
                    let scale = 2; // Adjust the scale as needed

                    let pageViewPort = page.getViewport({ scale });

                    pdfCanvas.width = pageViewPort.width;
                    pdfCanvas.height = pageViewPort.height;

                    pdfCanvas.style.display = "block";
                    pdfCanvas.style.margin = "10px auto";
                    pdfCanvas.style.width = "80%"; // Adjust width as needed

                    $(".pdf-container").append(pdfCanvas);

                    page.render({
                        canvasContext: context,
                        viewport: pageViewPort
                    });
                }).catch(pageErr => {
                    console.log(pageErr);
                });
            }
        }).catch(pdfErr => {
            console.log(pdfErr);
        });

        $("body").append(watermark);
    }

    const url = pdfUrl();
    if (url) {
        initPDFViewer(url);
    }
});













// let watermark = document.createElement("p");
//         let watermark1 = document.createElement("p");
//         let watermark2 = document.createElement("p");
//         watermark.classList.add("watermark"); 
//         watermark1.classList.add("watermark"); 
//         watermark2.classList.add("watermark"); 
//         watermark.textContent="StudySync StudySync StudySync ";
//         watermark1.textContent="StudySync StudySync StudySync ";
//         watermark2.textContent="StudySync StudySync StudySync ";
//         watermark.style.top="-103px";
//         watermark.style.left="0px";
//         watermark1.style.top="183px";
//         watermark1.style.left="250px";
//         watermark2.style.top="306px";
//         watermark2.style.left="650px";
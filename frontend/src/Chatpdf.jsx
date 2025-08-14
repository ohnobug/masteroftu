import React, { PureComponent } from 'react';
import styles from './Chatpdf.module.less';

import { Document, Page, pdfjs } from "react-pdf";
pdfjs.GlobalWorkerOptions.workerSrc = `/pdf.worker.mjs`;

class Chatpdf extends PureComponent {
    state = {
        pageNumber: 1,
        pageNumberInput: 1,
        pageNumberFocus: false,
        numPages: 1,
        pageWidth: 600,
        fullscreen: false
    };

    onDocumentLoadSuccess = ({ numPages }) => {
        this.setState({ numPages: numPages })
    }

    lastPage = () => {
        if (this.state.pageNumber == 1) {
            return
        }
        const page = this.state.pageNumber - 1
        this.setState({ pageNumber: page, pageNumberInput: page })
    }

    nextPage = () => {
        if (this.state.pageNumber == this.state.numPages) {
            return
        }
        const page = this.state.pageNumber + 1
        this.setState({ pageNumber: page, pageNumberInput: page })
    }

    onPageNumberFocus = e => {
        this.setState({ pageNumberFocus: true })
    };

    onPageNumberBlur = e => {
        this.setState({ pageNumberFocus: false, pageNumberInput: this.state.pageNumber })
    };

    onPageNumberChange = e => {
        let value = e.target.value
        value = value <= 0 ? 1 : value;
        value = value >= this.state.numPages ? this.state.numPages : value;
        this.setState({ pageNumberInput: value })
    };

    toPage = e => {
        this.setState({ pageNumber: Number(e.target.value) })
    };

    pageZoomOut = () => {
        if (this.state.pageWidth <= 600) {
            return
        }
        const pageWidth = this.state.pageWidth * 0.8
        this.setState({ pageWidth: pageWidth })
    }

    pageZoomIn = () => {
        const pageWidth = this.state.pageWidth * 1.2
        this.setState({ pageWidth: pageWidth })
    }

    pageFullscreen = () => {
        if (this.state.fullscreen) {
            this.setState({ fullscreen: false, pageWidth: 600 })
        } else {
            this.setState({ fullscreen: true, pageWidth: window.screen.width - 40 })
        }
    }

    render() {
        const { pageNumber, pageNumberFocus, pageNumberInput, numPages, pageWidth, fullscreen } = this.state;
        return (
            <div className={styles.view}>
                <div className={styles.pageContainer}>
                    <Document
                        file="/1.pdf"
                        onLoadSuccess={this.onDocumentLoadSuccess}
                        loading={<span>加载中...</span>}
                        scale={1.6}
                    >
                        <Page pageNumber={pageNumber} width={pageWidth} loading={<span>加载中...</span>} />
                    </Document>
                </div>

                <div className={styles.pageTool}>
                    <button className={styles.pdfbutton} onClick={this.lastPage}>{pageNumber == 1 ? "已是第一页" : "上一页"}</button>

                    <span className={styles.pageinfo}>
                        <input value={pageNumberFocus ? pageNumberInput : pageNumber}
                            onFocus={this.onPageNumberFocus}
                            onBlur={this.onPageNumberBlur}
                            onChange={this.onPageNumberChange}
                            onPressEnter={this.toPage} type="number" /> / {numPages}
                    </span>


                    <button className={styles.pdfbutton} onClick={this.nextPage}>{pageNumber == numPages ? "已是最后一页" : "下一页"}</button>
                    <button className={styles.pdfbutton} onClick={this.pageZoomIn}>放大</button>
                    <button className={styles.pdfbutton} onClick={this.pageZoomOut}>缩小</button>
                    <button className={styles.pdfbutton} type={fullscreen ? "fullscreen-exit" : 'fullscreen'} onClick={this.pageFullscreen}>{fullscreen ? "恢复默认" : '适合窗口'}</button>
                </div>
            </div>
        );
    }
}

export default props => (
    <Chatpdf {...props} />
);

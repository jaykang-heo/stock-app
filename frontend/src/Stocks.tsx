import React, { ButtonHTMLAttributes, FC, useState } from 'react';
import axios from 'axios';
import styles from './Stocks.module.css';

interface PrettyButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
    onClick: (event: React.MouseEvent<HTMLButtonElement>) => void;
}

const PrettyButton: FC<PrettyButtonProps> = ({ onClick, children }) => (
    <button className={styles.button} onClick={onClick}>
        {children}
    </button>
);

const Stocks: React.FC = () => {
    const [jangtaStocks, setJangtaStocks] = useState<string[]>([]);
    const [loading, setLoading] = useState(false);
    const [, setFileName] = useState<string>("");
    const [daysAgo, setDaysAgo] = useState<number>(2);

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFile = event.target.files?.[0];
        if (selectedFile) {
            setFileName(selectedFile.name);
        }
    };

    const handleUploadFile = async () => {
        setJangtaStocks([]);

        const selectedFile = document.querySelector<HTMLInputElement>('#fileInput')?.files?.[0];
        if (!selectedFile) return;

        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            await axios.post('http://localhost:8000/upload-csv/', formData);
            fetchJangtaData();
        } catch (error) {
            console.error("Error uploading file:", error);
        }
    };

    const fetchJangtaData = async () => {
        setLoading(true);
        try {
            const response = await axios.get(`http://localhost:8000/stocks/jangta/?days_ago=${daysAgo}`);
            setJangtaStocks(response.data);
        } catch (error) {
            console.error("Error fetching jangta stocks:", error);
        } finally {
            setLoading(false);
        }
    };

    const computeDaysAgo = (selectedDate: Date) => {
        const now = new Date();
        const diffTime = Math.abs(now.getTime() - selectedDate.getTime());
        return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    };

    const handleDateChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const selectedDate = new Date(event.target.value);
        setDaysAgo(computeDaysAgo(selectedDate));
    };

    const parseJangtaStock = (stock: string) => {
        const matches = stock.match(/\('([^']*)', '([^']*)', (-?\d+(\.\d+)?),? ?(-?\d+(\.\d+)?)?,? ?(-?\d+(\.\d+)?)?\)/);
        return matches ? [matches[1], matches[2], Number(matches[3]), Number(matches[5]) || 0, Number(matches[7]) || 0] : ["", "", 0, 0, 0];
    };

    const handleNameClick = async (stockCode: string) => {
        try {
            await axios.get(`http://localhost:8000/stocks/chart/candle/${stockCode}`);
        } catch (error) {
            console.error(`Error fetching details for stock code ${stockCode}:`, error);
        }
    };

    return (
        <div className={styles.container}>
            <h2 className={styles.title}>Filtered Stocks</h2>
            <label className={styles.label}>
                Select Date:
                <input type="date" className={styles.prettyInput} onChange={handleDateChange} />
            </label>
            <br />
            <label className={styles.uploadLabel} htmlFor="fileInput">
                Choose CSV
            </label>
            <input type="file" id="fileInput" onChange={handleFileChange} className={styles.hiddenInput} />
            <PrettyButton onClick={handleUploadFile}>Upload CSV</PrettyButton>
            {loading && <p>Loading...</p>}
            <div className={styles.flexContainer}>
                <div className={styles.tableContainer}>
                    <h3>Jangta Stocks {jangtaStocks.length > 0 && <span>- Complete</span>}</h3>
                    <table className={styles.table}>
                        <thead>
                            <tr>
                                <th>Stock Code</th>
                            </tr>
                        </thead>
                        <tbody>
                            {jangtaStocks.map(stock => {
                                const [name, code, volume, diff, line] = parseJangtaStock(stock);
                                return (
                                    <tr key={code}>
                                        <td>{name}</td>
                                        <td>{code}</td>
                                        <td>{volume}</td>
                                        <td>{diff}</td>
                                        <td>{line}</td>
                                    </tr>
                                );
                            })}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}

export default Stocks;

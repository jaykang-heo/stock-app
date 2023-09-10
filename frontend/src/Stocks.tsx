import React, { useState } from 'react';
import axios from 'axios';
import styles from './Stocks.module.css';

const Stocks: React.FC = () => {
    const [stocks, setStocks] = useState<string[]>([]);
    const [loading, setLoading] = useState(false);
    const [fileName, setFileName] = useState<string>("");
    const [daysAgo, setDaysAgo] = useState<number>(2);


    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFile = event.target.files && event.target.files[0];
        if (selectedFile) {
            setFileName(selectedFile.name);
        }
    };

    const handleUploadFile = async () => {
        const selectedFile = document.querySelector<HTMLInputElement>('#fileInput')?.files?.[0];
        if (!selectedFile) {
            console.error("No file selected");
            return;
        }

        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            const response = await axios.post('http://localhost:8000/upload-csv/', formData);
            console.log(response.data);
            fetchData();  // Fetch the stock data after uploading the file
        } catch (error) {
            console.error("Error uploading file:", error);
        }
    };

    const handleDaysAgoChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setDaysAgo(Number(event.target.value));
    };

    const fetchData = async () => {
        setLoading(true);
        try {
            const response = await axios.get(`http://localhost:8000/stocks/?days_ago=${daysAgo}`);
            setStocks(response.data);
        } catch (error) {
            console.error("Error fetching stocks:", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className={styles.container}>
            <h2 className={styles.title}>Filtered Stocks</h2>

            {/*<button className={styles.button} onClick={fetchData}>*/}
            {/*    Fetch Stocks*/}
            {/*</button>*/}

            <label>
                Days Ago:
                <input type="number" value={daysAgo} onChange={handleDaysAgoChange} />
            </label>

            <input type="file" id="fileInput" onChange={handleFileChange} />
            <button onClick={handleUploadFile}>Upload CSV</button>

            {loading && <p>Loading...</p>}

            <table className={styles.table}>
                <thead>
                <tr>
                    <th>Stock Code</th>
                </tr>
                </thead>
                <tbody>
                {stocks.map(stock => (
                    <tr key={stock}>
                        <td>{stock}</td>
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
    );
}

export default Stocks;

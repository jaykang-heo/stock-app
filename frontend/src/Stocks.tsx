import React, { useState } from 'react';
import axios from 'axios';
import styles from './Stocks.module.css';

const Stocks: React.FC = () => {
    const [stocks, setStocks] = useState<string[]>([]);
    const [jangtaStocks, setJangtaStocks] = useState<string[]>([]);
    const [loading, setLoading] = useState(false);
    const [fileName, setFileName] = useState<string>("");
    const [daysAgo, setDaysAgo] = useState<number>(2);
    const [channelRangeStocks, setChannelRangeStocks] = useState<string[]>([]);


    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFile = event.target.files && event.target.files[0];
        if (selectedFile) {
            setFileName(selectedFile.name);
        }
    };

     const fetchChannelRangeData = async () => {
        setLoading(true);
        try {
            const response = await axios.get('http://localhost:8000/stocks/within-channel-range');
            setChannelRangeStocks(response.data);
        } catch (error) {
            console.error("Error fetching stocks within channel range:", error);
        } finally {
            setLoading(false);
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
            fetchJangtaData();  // Fetch the jangta stock data after uploading the file
            fetchData();  // Fetch the danta stock data after uploading the file
            fetchChannelRangeData();
        } catch (error) {
            console.error("Error uploading file:", error);
        }
    };

    const handleDaysAgoChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setDaysAgo(Number(event.target.value));
    };

    const fetchJangtaData = async () => {
        setLoading(true);
        try {
            const response = await axios.get('http://localhost:8000/stocks/jangta/');
            setJangtaStocks(response.data);
        } catch (error) {
            console.error("Error fetching jangta stocks:", error);
        } finally {
            setLoading(false);
        }
    };

    const fetchData = async () => {
        setLoading(true);
        try {
            const response = await axios.get(`http://localhost:8000/stocks/danta/?days_ago=${daysAgo}`);
            setStocks(response.data);
        } catch (error) {
            console.error("Error fetching danta stocks:", error);
        } finally {
            setLoading(false);
        }
    };

    return (
    <div className={styles.container}>
        <h2 className={styles.title}>Filtered Stocks</h2>

        <label>
            Days Ago:
            <input type="number" value={daysAgo} onChange={handleDaysAgoChange} />
        </label>
        <input type="file" id="fileInput" onChange={handleFileChange} />
        <button onClick={handleUploadFile}>Upload CSV</button>
        {loading && <p>Loading...</p>}

        <div className={styles.flexContainer}>
            {/* Jangta Stocks Column */}
            <div className={styles.tableContainer}>
                <h3>Jangta Stocks</h3>
                <table className={styles.table}>
                    <thead>
                        <tr>
                            <th>Stock Code</th>
                        </tr>
                    </thead>
                    <tbody>
                        {jangtaStocks.map(stock => (
                            <tr key={stock}>
                                <td>{stock}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {/* Danta Stocks Column */}
            <div className={styles.tableContainer}>
                <h3>Danta Stocks</h3>
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

            {/* Stocks Within ±5% of Lower Channel Column */}
            <div className={styles.tableContainer}>
                <h3>Stocks Within ±7% of Lower Channel</h3>
                <table className={styles.table}>
                    <thead>
                        <tr>
                            <th>Stock Code</th>
                        </tr>
                    </thead>
                    <tbody>
                        {channelRangeStocks.map(stock => (
                            <tr key={stock}>
                                <td>{stock}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
);}

export default Stocks;

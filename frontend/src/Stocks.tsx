import React, {ButtonHTMLAttributes, FC, useState} from 'react';
import axios from 'axios';
import styles from './Stocks.module.css';
import {match} from "node:assert";


interface PrettyButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
    onClick: (event: React.MouseEvent<HTMLButtonElement>) => void;
}

const PrettyButton: FC<PrettyButtonProps> = ({ onClick, children }) => {
    return (
        <button className={styles.button} onClick={onClick}>
            {children}
        </button>
    );
};


const Stocks: React.FC = () => {
    const [stocks, setStocks] = useState<string[]>([]);
    const [jangtaStocks, setJangtaStocks] = useState<string[]>([]);
    const [loading, setLoading] = useState(false);
    const [fileName, setFileName] = useState<string>("");
    const [daysAgo, setDaysAgo] = useState<number>(2);
    const [channelRangeStocks, setChannelRangeStocks] = useState<string[]>([]);
    const [joongtaStocks, setJoongtaStocks] = useState<string[]>([]);
    const [selectedDate, setSelectedDate] = useState<string>(""); // New date state




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

     const fetchJoongtaData = async (filePath: string) => {
    setLoading(true);
    try {
        const response = await axios.get(`http://localhost:8000/stocks/joongta?file_path=${filePath}`);
        setJoongtaStocks(response.data);
    } catch (error) {
        console.error("Error fetching joongta stocks:", error);
    } finally {
        setLoading(false);
    }
};


    const handleUploadFile = async () => {
    // Clear previous stocks data
    setStocks([]);
    setJangtaStocks([]);
    setChannelRangeStocks([]);

    const selectedFile = document.querySelector<HTMLInputElement>('#fileInput')?.files?.[0];
    if (!selectedFile) {
        console.error("No file selected");
        return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);
    console.log(selectedFile)
    console.log(formData)

    try {
        const response = await axios.post('http://localhost:8000/upload-csv/', formData);
        console.log(response.data);
        fetchJangtaData();  // Fetch the jangta stock data after uploading the file
        // fetchData();  // Fetch the danta stock data after uploading the file
        // fetchChannelRangeData();
        // fetchJoongtaData(fileName);  // Fetch the joongta stock data after uploading the file

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
            const response = await axios.get(`http://localhost:8000/stocks/jangta/?days_ago=${daysAgo}`);
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

        const computeDaysAgo = (selectedDate: Date) => {
        const now = new Date();
        const diffTime = Math.abs(now.getTime() - selectedDate.getTime());
        return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    };

    // Update your change handler
    const handleDateChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const selectedDate = new Date(event.target.value);
        const days = computeDaysAgo(selectedDate);
        setDaysAgo(days);
    };

   const parseStock = (stock: string): [string, string, number, number?] => {
        const matches = stock.match(/\('([^']*)', '([^']*)', (\d+(\.\d+)?),? ?(\d+(\.\d+)?)?\)/);
        if (matches) {
            return [matches[1], matches[2], Number(matches[3]), matches[5] ? Number(matches[5]) : undefined];
        }
        return ["", "", 0];
    };

    const parseJangtaStock = (stock: string): [string, string, number, number, number] => {
        console.log(stock)
        const matches = stock.match(/\('([^']*)', '([^']*)', (-?\d+(\.\d+)?),? ?(-?\d+(\.\d+)?)?,? ?(-?\d+(\.\d+)?)?\)/);
        if (matches) {
            return [matches[1], matches[2], Number(matches[3]), Number(matches[5]) || 0, Number(matches[7]) || 0];
        }
        return ["", "", 0, 0, 0];
    };


   const handleNameClick = async (stockCode: string) => {
        try {
            const response = await axios.get(`http://localhost:8000/stocks/chart/candle/${stockCode}`);
            console.log(response.data);
        } catch (error) {
            console.error(`Error fetching details for stock code ${stockCode}:`, error);
        }
    };



    return (
    <div className={styles.container}>
            <h2 className={styles.title}>Filtered Stocks</h2>

            <label className={styles.label}>
                Select Date:
                <input
                    type="date"
                    className={styles.prettyInput}
                    onChange={handleDateChange}
                />
            </label>
            <br/>
            <label className={styles.uploadLabel} htmlFor="fileInput">
                Choose CSV
            </label>
            <input type="file" id="fileInput" onChange={handleFileChange} className={styles.hiddenInput} />

            <PrettyButton onClick={handleUploadFile}>Upload CSV</PrettyButton>
        {loading && <p>Loading...</p>}

        <div className={styles.flexContainer}>
            {/* Jangta Stocks Column */}
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
                                <tr key={""}>
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
            {/* Joongta Stocks Column */}
{/*<div className={styles.tableContainer}>*/}
{/*    <h3>Joongta Stocks {joongtaStocks.length > 0 && <span>- Complete</span>}</h3>*/}
{/*    <table className={styles.table}>*/}
{/*        <thead>*/}
{/*            <tr>*/}
{/*                <th>Name</th>*/}
{/*                <th>Code</th>*/}
{/*                <th>Number</th>*/}
{/*            </tr>*/}
{/*        </thead>*/}
{/*        <tbody>*/}
{/*            {joongtaStocks.map(stock => {*/}
{/*                const [name, code, volume] = parseStock(stock);*/}
{/*                return (*/}
{/*                    <tr key={code}>*/}
{/*                        <td>{name}</td>*/}
{/*                        <td>{code}</td>*/}
{/*                        <td>{volume}</td>*/}
{/*                    </tr>*/}
{/*                );*/}
{/*            })}*/}
{/*        </tbody>*/}
{/*    </table>*/}
{/*</div>*/}

            {/* Danta Stocks Column */}
            <div className={styles.tableContainer}>
                <h3>Danta Stocks {stocks.length > 0 && <span>- Complete</span>}</h3>
                <table className={styles.table}>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Code</th>
                            <th>Number</th>
                        </tr>
                    </thead>
                    <tbody>
                        {stocks.map(stock => {
                            const [name, code, volume] = parseStock(stock);
                            return (
                                <tr key={code}>
                                    <td>{name}</td>
                                    <td>{code}</td>
                                    <td>{volume}</td>
                                </tr>
                            );
                        })}
                    </tbody>
                </table>
            </div>

            {/* Stocks Within ±7% of Lower Channel Column */}
            <div className={styles.tableContainer}>
                <h3>Joongta {channelRangeStocks.length > 0 && <span>- Complete</span>}</h3>
                <table className={styles.table}>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Code</th>
                            <th>Number</th>
                            <th>Value</th>
                        </tr>
                    </thead>
                    <tbody>
                        {channelRangeStocks.map(stock => {
                            const [name, code, volume, percent] = parseStock(stock);
                            return (
                                <tr key={code}>
                                    <td onClick={() => handleNameClick(code)} style={{cursor: 'pointer'}}>{name}</td>
                                    <td>{code}</td>
                                    <td>{volume}</td>
                                    <td>{percent}</td>
                                </tr>
                            );
                        })}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
);}

export default Stocks;

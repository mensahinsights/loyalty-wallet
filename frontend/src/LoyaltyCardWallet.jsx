import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import Quagga from 'quagga';

export default function LoyaltyCardWallet() {
  const [cards, setCards] = useState([]);
  const [form, setForm] = useState({ name: '', barcode: '', image: null });
  const [showScanner, setShowScanner] = useState(false);
  const scannerRef = useRef(null);

  useEffect(() => {
    fetchCards();
  }, []);

  const fetchCards = async () => {
    const res = await axios.get('/api/cards');
    setCards(res.data);
  };

  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append('name', form.name);
    formData.append('barcode', form.barcode);
    formData.append('image', form.image);

    await axios.post('/api/cards', formData);
    setForm({ name: '', barcode: '', image: null });
    fetchCards();
  };

  const handleDelete = async (id) => {
    await axios.delete(`/api/cards/${id}`);
    fetchCards();
  };

  const startScanner = () => {
    Quagga.init({
      inputStream: { type: 'LiveStream', target: scannerRef.current },
      decoder: { readers: ['code_128_reader', 'ean_reader', 'qr_reader'] }
    }, err => {
      if (!err) Quagga.start();
    });

    Quagga.onDetected(result => {
      setForm(prev => ({ ...prev, barcode: result.codeResult.code }));
      Quagga.stop();
      setShowScanner(false);
    });
  };

  return (
    <div className="p-4">
      <h1>Loyalty Card Wallet</h1>
      <input
        placeholder="Card Name"
        value={form.name}
        onChange={e => setForm({ ...form, name: e.target.value })}
      /><br />
      <input
        placeholder="Barcode"
        value={form.barcode}
        onChange={e => setForm({ ...form, barcode: e.target.value })}
      />
      <button onClick={() => setShowScanner(!showScanner)}>Scan Barcode</button><br />
      {showScanner && <div ref={scannerRef} style={{ width: '300px', height: '200px' }} />}
      <input
        type="file"
        onChange={e => setForm({ ...form, image: e.target.files[0] })}
      /><br />
      <button onClick={handleSubmit}>Save Card</button>

      <ul>
        {cards.map(card => (
          <li key={card.id}>
            <strong>{card.name}</strong><br />
            Barcode: {card.barcode}<br />
            <img src={`/uploads/${card.image}`} alt={card.name} width="200" /><br />
            <button onClick={() => handleDelete(card.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

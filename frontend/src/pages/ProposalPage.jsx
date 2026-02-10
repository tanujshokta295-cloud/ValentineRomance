import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import axios from 'axios';
import { Heart, ArrowLeft } from 'lucide-react';
import { Button } from '../components/ui/button';
import FloatingHearts from '../components/FloatingHearts';
import ProposalCard from '../components/ProposalCard';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const ProposalPage = () => {
  const { proposalId } = useParams();
  const navigate = useNavigate();
  const [proposal, setProposal] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProposal = async () => {
      try {
        const response = await axios.get(`${API}/proposals/${proposalId}`);
        setProposal(response.data);
      } catch (err) {
        console.error('Error fetching proposal:', err);
        if (err.response?.status === 404) {
          setError('This proposal was not found. It may have been removed or the link is incorrect.');
        } else {
          setError('Something went wrong. Please try again later.');
        }
      } finally {
        setLoading(false);
      }
    };

    if (proposalId) {
      fetchProposal();
    }
  }, [proposalId]);

  const handleAccept = async () => {
    try {
      await axios.patch(`${API}/proposals/${proposalId}`, {
        accepted: true,
      });
    } catch (err) {
      console.error('Error updating proposal:', err);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#FFF0F5] flex items-center justify-center">
        <motion.div
          animate={{ scale: [1, 1.2, 1] }}
          transition={{ duration: 1, repeat: Infinity }}
        >
          <Heart className="text-[#FF4D6D] fill-[#FF4D6D]" size={64} />
        </motion.div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-[#FFF0F5] flex items-center justify-center px-4">
        <FloatingHearts />
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="valentine-card p-8 md:p-12 max-w-md w-full text-center relative z-10"
        >
          <div className="text-6xl mb-6">💔</div>
          <h2 className="font-heading text-2xl font-bold text-gray-700 mb-4">
            Oops!
          </h2>
          <p className="font-body text-gray-600 mb-6">{error}</p>
          <Button
            onClick={() => navigate('/')}
            className="valentine-btn-yes"
            data-testid="go-home-btn"
          >
            <ArrowLeft size={18} className="mr-2" />
            Create Your Own Proposal
          </Button>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#FFF0F5] flex items-center justify-center px-4 py-8">
      <FloatingHearts />
      <div className="relative z-10 w-full">
        <ProposalCard
          valentineName={proposal.valentine_name}
          customMessage={proposal.custom_message}
          characterChoice={proposal.character_choice}
          onAccept={handleAccept}
        />
      </div>
    </div>
  );
};

export default ProposalPage;

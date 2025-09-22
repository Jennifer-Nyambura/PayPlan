"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useAuth } from "../../context/AuthContext";
import { DollarSign, Calendar, AlertTriangle, TrendingUp } from "lucide-react";
import Navbar from "../../Components/Navbar";
import ServiceCard from "../../Components/ServiceCard";
import PaymentItem from "../../Components/PaymentItem";
import StatsCard from "../../Components/StatsCard";
import {getServices, getUpcomingPayments, getOverduePayments, markPaymentAsPaid} from "../../utils/api";

export default function DashboardPage() {
  const { user, token } = useAuth();

  const [services, setServices] = useState([]);
  const [upcomingPayments, setUpcomingPayments] = useState([]);
  const [overduePayments, setOverduePayments] = useState([]);
  const [loading, setLoading] = useState(true);

  const formatCurrency = (amount) =>
    new Intl.NumberFormat("en-KE", {
      style: "currency",
      currency: "KES",
      minimumFractionDigits: 0,
    }).format(amount);

  // Fetch data from backend when dashboard loads
  useEffect(() => {
    const fetchData = async () => {
      try {
        const [servicesData, upcomingData, overdueData] = await Promise.all([
          getServices(token),
          getUpcomingPayments(token),
          getOverduePayments(token),
        ]);
        setServices(servicesData || []);
        setUpcomingPayments(upcomingData || []);
        setOverduePayments(overdueData || []);
      } catch (error) {
        console.error("Error loading dashboard data:", error);
      } finally {
        setLoading(false);
      }
    };

    if (user && token) fetchData(); 
  }, [user, token]);

  // Calculate monthly total dynamically
  const totalMonthlyAmount = services.reduce(
    (sum, service) => sum + (service.monthlyCost || 0),
    0
  );

  // Payment handler (mark as paid)
  const handleMarkAsPaid = async (paymentId) => {
    try {
      await markPaymentAsPaid(paymentId, token);
      // Refresh lists after marking payment
      const [servicesData, upcomingData, overdueData] = await Promise.all([
        getServices(token),
        getUpcomingPayments(token),
        getOverduePayments(token),
      ]);
      setServices(servicesData || []);
      setUpcomingPayments(upcomingData || []);
      setOverduePayments(overdueData || []);
    } catch (error) {
      console.error("Failed to mark payment as paid:", error);
    }
  };

  const recentServices = services.slice(0, 3);
  const nextPayments = upcomingPayments.slice(0, 3);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-black to-gray-900">
        <p className="text-white/70">Loading your dashboard...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-black to-gray-900 px-6 py-6">
      <Navbar />

      <div className="mb-6">
        <h1 className="text-3xl font-bold text-white">Dashboard</h1>
        <p className="text-white/70">Manage your recurring payments</p>
      </div>

      {/* Stats Section */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-10">
        <StatsCard
          title="Monthly Total"
          value={formatCurrency(totalMonthlyAmount)}
          subtitle="Estimated monthly spending"
          icon={<DollarSign className="w-5 h-5 text-white" />}
          cardClass="backdrop-blur-xl bg-white/5 border border-white/10"
        />
        <StatsCard
          title="Active Services"
          value={services.length.toString()}
          subtitle="Subscriptions & services"
          icon={<TrendingUp className="w-5 h-5 text-white" />}
          cardClass="backdrop-blur-xl bg-white/5 border border-white/10"
        />
        <StatsCard
          title="Due Soon"
          value={upcomingPayments.length.toString()}
          subtitle="Next 30 days"
          icon={<Calendar className="w-5 h-5 text-white" />}
          cardClass="backdrop-blur-xl bg-white/5 border border-white/10"
        />
        <StatsCard
          title="Overdue"
          value={overduePayments.length.toString()}
          subtitle="Needs attention"
          icon={<AlertTriangle className="w-5 h-5 text-white" />}
          cardClass="backdrop-blur-xl bg-white/5 border border-white/10"
        />
      </div>

      {/* Overdue Payments */}
      {overduePayments.length > 0 && (
        <section className="mb-10">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold text-white">
              ⚠️ Overdue Payments
            </h2>
          </div>
          <div className="space-y-3">
            {overduePayments.map((payment) => (
              <PaymentItem
                key={payment.id}
                payment={payment}
                onMarkAsPaid={handleMarkAsPaid}
                cardClass="backdrop-blur-sm bg-white/5 border border-white/10"
                textClass="text-white"
              />
            ))}
          </div>
        </section>
      )}

      {/* Upcoming Payments */}
      {nextPayments.length > 0 && (
        <section className="mb-10">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold text-white">
              Upcoming Payments
            </h2>
            {upcomingPayments.length > 3 && (
              <Link
                href="/upcoming"
                className="text-red-400 font-medium hover:text-red-500"
              >
                See All
              </Link>
            )}
          </div>
          <div className="space-y-3">
            {nextPayments.map((payment) => (
              <PaymentItem
                key={payment.id}
                payment={payment}
                onMarkAsPaid={handleMarkAsPaid}
                cardClass="backdrop-blur-sm bg-white/5 border border-white/10"
                textClass="text-white"
              />
            ))}
          </div>
        </section>
      )}

      {/* Recent Services */}
      {recentServices.length > 0 && (
        <section className="mb-10">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold text-white">Your Services</h2>
            {services.length > 3 && (
              <Link
                href="/services"
                className="text-red-400 font-medium hover:text-red-500"
              >
                See All
              </Link>
            )}
          </div>
          <div className="space-y-3">
            {recentServices.map((service) => (
              <ServiceCard
                key={service.id}
                service={service}
                cardClass="backdrop-blur-sm bg-white/5 border border-white/10"
                textClass="text-white"
              />
            ))}
          </div>
        </section>
      )}

      {/* Empty State */}
      {services.length === 0 && (
        <div className="text-center mt-20">
          <h2 className="text-2xl font-bold text-white">Welcome to PayPlan!</h2>
          <p className="text-white/70 mt-2">
            Start by adding your first subscription or recurring service.
          </p>
          <Link
            href="/services"
            className="mt-4 inline-block text-red-400 font-semibold hover:text-red-500"
          >
            Add Your First Service →
          </Link>
        </div>
      )}
    </div>
  );
}

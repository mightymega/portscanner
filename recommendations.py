# recommendations.py

def get_recommendations(port):
    recommendations = {
        22: "SSH is open. Consider changing the default port, disabling root login, and using key-based authentication.",
        80: "HTTP is open. Ensure you have a secure web server and consider redirecting to HTTPS.",
        443: "HTTPS is open. Ensure your SSL certificate is up-to-date.",
        3306: "MySQL is open. Restrict access to trusted IPs and disable remote root login.",
        3389: "RDP is open. Use a VPN and enable network-level authentication.",
    }

    return recommendations.get(port, "No specific recommendation, but ensure this port is needed and properly secured.")

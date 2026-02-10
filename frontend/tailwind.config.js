/** @type {import('tailwindcss').Config} */
module.exports = {
    darkMode: ["class"],
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
    	extend: {
    		fontFamily: {
    			heading: ['Nunito', 'sans-serif'],
    			body: ['Quicksand', 'sans-serif'],
    		},
    		colors: {
    			valentine: {
    				bg: '#FFF0F5',
    				surface: '#FFFFFF',
    				primary: '#FF4D6D',
    				'primary-hover': '#FF3355',
    				secondary: '#FF8FA3',
    				text: '#4A4A4A',
    				'text-muted': '#8A8A8A',
    			},
    		},
    		borderRadius: {
    			lg: 'var(--radius)',
    			md: 'calc(var(--radius) - 2px)',
    			sm: 'calc(var(--radius) - 4px)'
    		}
    	}
    },
    plugins: [require("tailwindcss-animate")],
}

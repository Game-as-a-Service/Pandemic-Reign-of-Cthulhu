import type { Metadata } from 'next'
import { Source_Sans_3, Aladin } from 'next/font/google'
import './globals.css'
import { cn } from '@/lib/utils'

export const metadata: Metadata = {
  title: 'Pandemic - Reign of Cthlthu',
  description: 'GaaS Side Project',
}

export const fontSans = Source_Sans_3({
  subsets: ["latin"],
  variable: "--font-sans",
})

export const fontDisplay = Aladin({
  subsets: ['latin'],
  weight: '400',
  variable: '--font-display'
})

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head />
      <body className={cn('min-h-screen bg-background font-sans antialiased', fontSans.variable, fontDisplay.variable)}>{children}</body>
    </html>
  )
}

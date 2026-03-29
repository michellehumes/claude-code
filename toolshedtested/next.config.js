/** @type {import('next').NextConfig} */
const nextConfig = {
  async redirects() {
    return [
      {
        source: '/buying-guides-hub',
        destination: '/buying-guides',
        permanent: true,
      },
      {
        source: '/tool-comparisons-hub',
        destination: '/category/comparisons',
        permanent: true,
      },
      {
        source: '/best-tool-deals',
        destination: '/deals',
        permanent: true,
      },
      {
        source: '/category/reviews',
        destination: '/reviews',
        permanent: true,
      },
      {
        source: '/category/buying-guides',
        destination: '/buying-guides',
        permanent: true,
      },
    ]
  },
}

module.exports = nextConfig

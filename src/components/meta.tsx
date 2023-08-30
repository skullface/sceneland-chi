import Head from 'next/head'

export const SiteMeta = () => {
  return (
    <Head>
      <title>312.show: Upcoming shows in Chicago</title>
      <meta
        name='description'
        content='Concerts and events coming up at your fav local venues like Thalia Hall, Empty Bottle, Subterranean, and more.'
      />
      <meta name='viewport' content='width=device-width, initial-scale=1' />
      <link rel='icon' href='/favicon.png' />
    </Head>
  )
}
